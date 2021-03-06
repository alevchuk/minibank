#!/usr/bin/python3

import time
import os
import logging
import glob

# Documentation is here https://github.com/alevchuk/minibank/blob/first/scripts/REMEDIATION.md

CPU_THRESHOLD_SECONDS = 0.3
POLL_INTERVAL_SECONDS = 15

# NOTE: remediation is too fast for most metrics to show that there was an actual issue
DETECTION_WINDOW_MINUTES = 4  # set window to 60 and min_datapoints to 200 if you want to test / see the issue in metrics
BLACKOUT_WINDOW_MINUTES = 60  # after remediation ran, how long to wait and not do aything
MIN_DATAPOINTS = 10  # the minimum number of data points to consider the alert to fire

DETECTION_WINDOW_PCT = 50  # If X% of data points are above the threshold then the detector fires

#LOG_LEVEL = logging.DEBUG
LOG_LEVEL = logging.INFO

logging.basicConfig(level=LOG_LEVEL, format='%(levelname).1s %(asctime)-15s %(pathname)s:%(lineno)s: %(message)s')
log = logging.getLogger("proc_stat")

# Parameter checking
max_num_datapoints =  int(DETECTION_WINDOW_MINUTES * 60 / POLL_INTERVAL_SECONDS)
assert max_num_datapoints > MIN_DATAPOINTS, \
    "MIN_DATAPOINTS should not exceed {} - the number of datapoint in the DETECTION_WINDOW".format(max_num_datapoints)


class Detector(object):
    def __init__(self, threshold, window_minutes, window_pct, min_datapoints):
        self.threshold = threshold
        self.detection_window = window_minutes
        self.window_pct = window_pct
        self.min_datapoints = min_datapoints
        self.condition = lambda value, threshold: value > threshold
        self.last_remediation_time = time.time()

        self.data = []

    def _cleanup(self):
        current_time = time.time()
        to_be_deleted = []

        for i, x in enumerate(self.data):
            # Keep 2x window in case we need to debug
            if x["ts"] < current_time - (self.detection_window * 60 * 2):
                to_be_deleted.append(i)

        log.debug("Deleting {} data points".format(len(to_be_deleted)))
        for i in sorted(to_be_deleted, reverse=True):
            log.debug("Deleted {}".format(self.data[i]))
            del self.data[i]

    def _detect(self):
        points_within_window = 0
        points_violate_threshold = 0

        for x in self.data:
            if x["ts"] > time.time() - (self.detection_window * 60):
                points_within_window += 1
                if self.condition(x["value"], self.threshold):
                    points_violate_threshold += 1

        if self.last_remediation_time + BLACKOUT_WINDOW_MINUTES * 60 > time.time():
            log.info(
                (
                    "Restart or last remediation was {:.2f} minutes ago, we're still in blackout period"
                ).format((time.time() - self.last_remediation_time) / 60.0)
            )

        elif points_within_window < self.min_datapoints:
            log.info("Not enough datapoints available")

        else:
            if (points_violate_threshold / points_within_window) * 100 >= self.window_pct:
                log.info(
                    (
                        "ALERT FIRED: {} of {} datapoint violated the threshold"
                    ).format(
                        points_violate_threshold,
                        points_within_window
                    )
                )
                self.last_remediation_time = time.time()

                return True

        return False

    def next(self, value):
        self.data.append({"ts": time.time(), "value": value})
        self._cleanup()

        return self._detect()


class LNDProc(object):
    def __init__(self):
        self.pid = self._find_proc()

    def _all_procs(self):
        pids = [line.split("/")[2] for line in glob.glob("/proc/*/comm")]
        return [int(p) for p in pids if p.isnumeric()]

    def _find_proc(self):
        all_procs = self._all_procs()
        for pid in all_procs:
            try:
                with open("/proc/{}/comm".format(pid)) as f:
                    if f.readline().strip() == "lnd":
                        return pid
            except FileNotFoundError:
                pass

    def kill(self):
        if self.pid is None:
            log.info("Cannot kill, PID is unknown")
            return

        log.info("Killing PID (with SIGTERM): {}".format(self.pid))

        try:
            os.kill(self.pid, 15)
        except ProcessLookupError:
            log.info("Process already dead")
            return

        pre_kill_sleep = 60
        log.info("Sleeping for {} seconds".format(pre_kill_sleep))
        time.sleep(POLL_INTERVAL_SECONDS)

        if self._find_proc() == self.pid:
            log.info("Process sitll running, killing PID (with SIGKILL): {}".format(self.pid))
            try:
                os.kill(self.pid, 9)
            except ProcessLookupError:
                pass


class Stats(object):
    def __init__(self):
        # get initial data point
        self.proc_stat_lines = self._read_proc_stat()
        self.cpu_stats = self._parse_cpu_stats()

        self.cpu_stats_prev = None

    def _read_proc_stat(self):
        with open("/proc/stat", "r") as proc:
            return proc.readlines()

    def _parse_cpu_stats(self):
        """
        Refer to http://www.linuxhowtos.org/manpages/5/proc.htm
        """
        cpu = {}

        row = self.proc_stat_lines[0].split()
        cpu["time"] = time.time()

        cpu["user"] = row[1]  # normal processes executing in user mode
        cpu["nice"] = row[2]  # niced processes executing in user mode
        cpu["system"] = row[3]  # processes executing in kernel mode
        cpu["idle"] = row[4]  # twiddling thumbs
        cpu["iowait"] = row[5]  # waiting for I/O to complete
        cpu["irq"] = row[6]  # servicing interrupts
        cpu["softirq"] = row[7]  #servicing softirqs
        cpu["steal"] = row[8] # ticks spent executing other virtual hosts (in virtualised environments like Xen)
        cpu["guest"] = row[9] # time spent running a virtual CPU for guest operating systems under the control of the Linux kernel

        for k in cpu.keys():
            cpu[k] = int(cpu[k])

        return cpu

    def get_cpu(self):
        """
        Intended to run X number of seconds after Stats is initalized.
        Where X is the time how long to sample for.
        """
        self.proc_stat_lines = self._read_proc_stat()

        self.cpu_stats_prev = self.cpu_stats
        self.cpu_stats = self._parse_cpu_stats()

        time_delta = self.cpu_stats["time"] - self.cpu_stats_prev["time"]

        deltas = {}
        for k in self.cpu_stats.keys():
            deltas[k] = self.cpu_stats[k] - self.cpu_stats_prev[k]

        return deltas


def main():
    stats = Stats()
    detector = Detector(
            threshold=CPU_THRESHOLD_SECONDS,
            window_minutes=DETECTION_WINDOW_MINUTES,
            window_pct=DETECTION_WINDOW_PCT,
            min_datapoints=MIN_DATAPOINTS
    )

    while True:
        log.info("Sleeping for {} seconds".format(POLL_INTERVAL_SECONDS))
        time.sleep(POLL_INTERVAL_SECONDS)

        cpu = stats.get_cpu()
        log.debug("Raw /proc/stat data: {}".format(cpu))

        total = cpu["user"] + cpu["nice"] + cpu["system"] + cpu["steal"]
        log.debug("Total CPU: {}".format(total))

        cpu_seconds = total / (POLL_INTERVAL_SECONDS * 100)
        log.info("CPU seconds: {:.2f}".format(cpu_seconds))

        lnd_proc = LNDProc()
        log.info("LND pid is: {}".format(lnd_proc.pid))
        if detector.next(cpu_seconds):
            lnd_proc.kill()


if __name__ == "__main__":
    main()
