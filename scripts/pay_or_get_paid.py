#!/usr/bin/python3

import time
import argparse
import socket
import subprocess
import json
import datetime
from os.path import expanduser
import sys
HOME = expanduser("~")

MSGLEN = 400
LOGFILE = HOME + "/pay_or_get_paid.py.log"

RUN_TRY_NUM = 12
RUN_TRY_SLEEP = 10

'''
Warning: This script opens a port that allows anyone to steal money from your LND wallet.
Yet, MICROPAYMENT_NUM_SAT is enforced, so even though anyone can easily steal from you,
they shouldn't be able to take more than MICROPAYMENT_NUM_SAT satoshi at a time.

The speed at which they can deplete your funds should be limited by the speed LN -
uy how many micropayments your lightning node can process in a given time.
'''
MICROPAYMENT_NUM_SAT = 1
NUM_PAYMENTS_PER_BATCH = 3  # switch payer and payee after every batch OR after payment failure
PAY_INVOICE_TIMEOUT = 2 * 60
TOTAL_TIMEOUT = 5 * 60

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, required=True)
parser.add_argument('-s', '--host', type=str)
parser.add_argument('-l', '--listen', action='store_true')

args = parser.parse_args()


def log(msg):
  timestamp = datetime.datetime.now()
  timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
  with open(LOGFILE, 'a') as w:
    msg = "{} {}".format(timestamp, msg)
    print(msg)
    w.write(msg + '\n')


def run(cmd, timeout=240):
  log("Running command: {}".format(cmd))
  accumulated_timeout = 0
  for _ in range(RUN_TRY_NUM):
    try_start = time.time()
    try:
      raw = subprocess.check_output(
               cmd,
               timeout=timeout
            ).decode("utf-8")
      break
    except Exception as e:
        print(e)
        print("Sleeping for {} seconds".format(RUN_TRY_SLEEP))
        time.sleep(RUN_TRY_SLEEP)

    try_duration = time.time() - try_start
    accumulated_timeout += try_duration

    if accumulated_timeout > timeout:
        raise Exception("Run command {} timeout after {} seconds".format(cmd, accumulated_timeout))

  else:
    raise Exception("Failed command: {}".format(cmd))

  return json.loads(raw)


def check_pay_ammount(pay_req):
    decoded = run(['lncli', 'decodepayreq', '--pay_req={}'.format(pay_req)])
    if int(decoded['num_satoshis']) != MICROPAYMENT_NUM_SAT:
        log("FATAL: No, thank you! We agreed that we pay {} sat at a time, and isntaed you requested {}".format(MICROPAYMENT_NUM_SAT, decoded))
        sys.exit(1)


class MySocket:
    """
      MySocket implementation from https://docs.python.org/2/howto/sockets.html#using-a-socket
      - coded for clarity, not efficiency
    """

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    @staticmethod
    def listen(port):
        # create an INET, STREAMing socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host,
        # and a well-known port
        serversocket.bind(('0.0.0.0', port))
        # become a server socket
        serversocket.listen(5)

        return serversocket

    def mysend(self, msg):
        if len(msg) < MSGLEN:
            msg += ' ' * (MSGLEN - len(msg))

        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(bytes(msg[totalsent:], 'UTF-8'))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return (b''.join(chunks)).decode('UTF-8').strip()


class PayPingPong(object):
    def __init__(self, mysocket, start_as_payee):
        self.mysocket = mysocket

        self.sat_paied = 0
        self.sat_received = 0
        self.drop = False
        self.retry = False

        self.payee = start_as_payee

    def run(self):
        while True:
            if self.payee:
                self.run_as_payee()
            else:
                self.run_as_payer()

    def run_as_payee(self):
        invoice_list = []
        for _ in range(NUM_PAYMENTS_PER_BATCH):
            invoice = run(['lncli', 'addinvoice', '{}'.format(MICROPAYMENT_NUM_SAT)])
            invoice_list.append(invoice)
            print("Sending invoice: {}".format(invoice))
            self.mysocket.mysend(invoice['pay_req'])

        # Confirm that invoice was settled
        start_time = time.time()
        num_settled = 0
        for _ in range(TOTAL_TIMEOUT):
            invoices_done = []
            for invoice in invoice_list:
                invoice_status = \
                    run(['lncli', 'lookupinvoice', '{}'.format(invoice['r_hash'])])

                if invoice_status['settled']:
                    num_settled += 1
                    invoices_done.append(invoice)

            for invoice in invoices_done:
                invoice_list.remove(invoice)

            seconds_passed = time.time() - start_time
            if seconds_passed > TOTAL_TIMEOUT:
                log("Invoice check timeout after {} seconds".format(seconds_passed))
                break

            print("{} of {} settled after {} seconds (timeout triggering a switch will be at {} seconds)".format(
                  num_settled, NUM_PAYMENTS_PER_BATCH, seconds_passed, TOTAL_TIMEOUT))

            if num_settled == NUM_PAYMENTS_PER_BATCH:
                self.sat_received += (MICROPAYMENT_NUM_SAT * num_settled)

                print("All settled after {}s, issuing switch".format(seconds_passed))
                self.switch()
                return

            time.sleep(1)

        if num_settled != NUM_PAYMENTS_PER_BATCH:
            # not everything got payed, yet count any remaining invoices that were settled
            for invoice in invoice_list:
                invoice_status = \
                    run(['lncli', 'lookupinvoice', '{}'.format(invoice['r_hash'])])
                if invoice_status['settled']:
                    self.sat_received += MICROPAYMENT_NUM_SAT

            print("Cannot settle after {} seconds, issuing switch".format(seconds_passed))
            self.switch()
            return

    def run_as_payer(self):
        if not self.retry:
            pay_req = self.mysocket.myreceive()
            print("Got invoice: {}".format(pay_req))

        self.retry = False

        if pay_req == "switch":
          log("Switch was issued. Total sat_paied was {:,} ({:,} payments)".format(
            self.sat_paied,
            self.sat_paied / MICROPAYMENT_NUM_SAT))

          self.payee = True
          self.drop = False
          self.sat_paied = 0
          self.sat_received = 0

        elif self.drop:
            print("Dropping invoce {}".format(pay_req))
        else:

          check_pay_ammount(pay_req)

          try:
            result = run(['lncli', 'payinvoice', '-f', '{}'.format(pay_req)], timeout=PAY_INVOICE_TIMEOUT)
          except Exception as e:
            print(e)
            print("payinvoice FAILED: {}, dropping all further invoces until 'switch'!".format(e))
            self.drop = True
          else:
            if result['payment_error'] == '':
              self.sat_paied += MICROPAYMENT_NUM_SAT
            else:
              # most likely bitcoind is behind, try again in a little bit
              if result['payment_error'].startswith('FinalIncorrectCltvExpiry'):
                self.retry = True
              else:
                log("Could not pay invoice {} because {}, "
                      "dropping all further invoces until 'switch'!".format(
                          pay_req, result['payment_error']
                      )
                  )
                self.drop = True

    def switch(self):
        self.mysocket.mysend("switch")

        log("Switch. Total sat_received was {:,} ({:,} payments)".format(
          self.sat_received,
          self.sat_received / MICROPAYMENT_NUM_SAT))

        if self.payee:
            self.payee = False
        else:
            self.payee = True

        self.drop = False
        self.sat_paied = 0
        self.sat_received = 0


if args.listen:
  serversocket = MySocket.listen(args.port)
  #accept connections from outside
  (clientsocket, address) = serversocket.accept()

  s = MySocket(clientsocket)
  ping = s.myreceive()
  assert ping == 'ping'
  s.mysend("pong")

  start_as_payee = False

else:
  s = MySocket()
  s.connect(args.host, args.port)
  s.mysend("ping")
  pong = s.myreceive()
  assert pong == 'pong'

  start_as_payee = True


pay_ping_ping = PayPingPong(s, start_as_payee=start_as_payee)
pay_ping_ping.run()
