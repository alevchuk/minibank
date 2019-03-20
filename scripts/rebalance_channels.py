#!/usr/bin/python3

import subprocess
import json
import sys

def pretty(raw):
  return json.dumps(raw, sort_keys=True, indent=4, separators=(',', ': '))

def regenerate_fees(route, amt, fee):
  amt += fee
  len_hops = len(route["hops"])
  forward_fee = fee * (len_hops - 2)

  for hop_num, h in enumerate(route["hops"]):
    h["amt_to_forward"] = str(int((forward_fee + amt - fee) / 1000))
    h["amt_to_forward_msat"] = str(forward_fee + amt - fee)

    if hop_num < len_hops - 2:  # all but last two forward fees
      forward_fee -= fee

    if hop_num < len_hops - 1:  # all but last get the fee
      h["fee_msat"] = str(fee)
      h["fee"] = str(int(fee / 1000))
    else:
      h["fee"] = "0"
      h["fee_msat"] = "0"

  return route

def add_self_to_route(route, chan_capacity, chan_id, amt, fee, expiry):
  """
    amt is the final ammount that should get payed to self
    fee is the forwarding fee that should get offered to the node one before last in hops

    Example of a route:
        {
            "total_time_lock": 545659,
            "total_fees": "0",
            "total_amt": "40000",
            "hops": [
                {
                    "chan_id": "599693433058295809",
                    "chan_capacity": "80253",
                    "amt_to_forward": "40000",
                    "fee": "0",
                    "expiry": 545659,
                    "amt_to_forward_msat": "40000000",
                    "fee_msat": "0"
                }
            ],
            "total_fees_msat": "0",
            "total_amt_msat": "40000000"
        }
  """
  route["hops"][-1]["expiry"] = expiry
  route["hops"].append(
    {
      "chan_id": str(chan_id),
      "chan_capacity": str(chan_capacity),
      "expiry": expiry,
    }
  )

  route = regenerate_fees(route, amt, fee)

  total_fees = 0
  for h in route["hops"]:
    total_fees += int(h["fee_msat"])
  #total_fees *= 2

  route["total_fees_msat"] = str(total_fees)
  route["total_fees"] = str(int(total_fees / 1000))

  route["total_amt_msat"] = str(total_fees + amt)
  route["total_amt"] =  str(int((total_fees + amt) / 1000))

  return route

def pad(x):
  return str(x).rjust(10)

def pad_float(f):
  return "{:.2f}%".format(f).rjust(10)

def print_route(route):
  for name, val in route.items():
    if name != "hops":
      print("{}\t{}".format(name, val))

  print("\t".join([
    pad("hop_num"),
    pad("chan_capacity"),
    pad("amt_to_forward"),
    pad("fee"),
    pad("expiry"),
    pad("forward_msat"),
    pad("fee_msat"),
    "chan_id",
    ]))

  for hop_num , h in enumerate(route["hops"]):
    print("\t".join([
      pad(hop_num),
      pad(h["chan_capacity"]),
      pad(h["amt_to_forward"]),
      pad(h["fee"]),
      pad(h["expiry"]),
      pad(h["amt_to_forward_msat"]),
      pad(h["fee_msat"]),
      h["chan_id"],
    ]))

  print()


def print_channels(channels, remote_total):
    channels = sorted(channels, key=lambda c: int(c["remote_balance"]))
    print("           chan_id\tpubkey\t{}\t{}\t{}\tmini-id".format(pad("local"), pad("remote"), pad("remote-pct")))
    print("-" * 80)
    for c in channels:

      if remote_total > 0:
        ratio = pad_float(int(c["remote_balance"]) * 100 / remote_total)
      else:
        ratio = "N/A"

      print("\t".join([
        c["chan_id"],
        c["remote_pubkey"][:7],
        pad(c["local_balance"]),
        pad(c["remote_balance"]),
        ratio,
        str(c["orig_id"]),
      ]))



def active_channels_with_remote_balances(channels):
  results = []
  for c in channels:
    if c["active"] == True:
      if int(c["remote_balance"]) > 0:
        results.append(c)

  if len(results) == 0:
      print("ERROR: no channels with remote balances, so there is nothing to balance")

  return results


def main():
  # TODO: switch to "click" or "argparse" python library after documenting an easy way to install the dependency on any platform
  if len(sys.argv) > 1 and '--help' in sys.argv or '-h' in sys.argv:
    print("""
      rebalance_channels.py  - shift remote_balance capacity between owned channels by making lightning payments to self

      With no arguments, the current active channels will be listed.

      Required arguments:
      --src-mini-id  mini-id selecting the source channel from which to move remote balance
      --dst-mini-id  mini-id selecting the destination channel to which to move remote balance
      --dst-pct      desired percentage remote balance on the destination channel

      Optional arguments:
      --rid          route id, if you want to pick a specific route, otherwise the first route will be used

    """)
    sys.exit(1)

  if len(sys.argv) > 1 and '--testnet' in sys.argv:
    net = ['--network=testnet']
  else:
    net = []

  date = subprocess.check_output(["date", "+%Y-%m-%dT%H:%M:%S%z"]).decode("utf-8").strip()  # shows local Timezone
  channels = json.loads(subprocess.check_output(["lncli", "listchannels"]).decode("utf-8"))["channels"]
  # assign id based on original order, which is somewhat stable
  # this is mini_id which is indented to be easy to use
  for i in range(len(channels)):
    channels[i]["orig_id"] = i

  channels_with_remote = active_channels_with_remote_balances(channels)
  total_remote_balance = sum(int(c['remote_balance']) for c in channels_with_remote)

  if len(sys.argv) > 1 and '--src-mini-id' in sys.argv:
    if len(channels_with_remote) == 0:
      sys.exit(1)

    # parse src_mini_id
    src_mini_id = int(sys.argv[sys.argv.index('--src-mini-id') + 1])

    # parse dst_mini_id
    if '--dst-mini-id' not in sys.argv:
      print("ERROR: please also specify --dst-mini-id\nTip: see --help")
      sys.exit(1)
    else:
      dst_mini_id = int(sys.argv[sys.argv.index('--dst-mini-id') + 1])

    # parse dst_pct
    if '--dst-pct' not in sys.argv:
      print("ERROR: please also specify --dst-pct\nTip: see --help")
      sys.exit(1)
    else:
      dst_pct = float(sys.argv[sys.argv.index('--dst-pct') + 1])

    src_c = channels[src_mini_id]
    src_local_balance = int(src_c["local_balance"])
    src_remote_balance = int(src_c["remote_balance"])
    src_remote_pubkey = src_c["remote_pubkey"]
    print("Source channel:")
    for name, val in src_c.items():
      print("{}\t{}".format(name, val))
    print()

    dst_c = channels[dst_mini_id]
    dst_local_balance = int(dst_c["local_balance"])
    dst_remote_balance = int(dst_c["remote_balance"])
    dst_remote_pubkey = dst_c["remote_pubkey"]
    print("Destination channel:")
    for name, val in dst_c.items():
      print("{}\t{}".format(name, val))
    print()

    desired_amt = int(total_remote_balance * (dst_pct / 100.0))
    print("Destination remote balance {}, desired destination remote balance {}".format(dst_remote_balance, desired_amt))

    # Amount to transfer
    amt = desired_amt - dst_remote_balance

    # check that dst remote balance is less then desired amount
    if dst_remote_balance >= desired_amt:
      print("ERROR: destination channel already has {} remote balance, more then desired percentage".format(dst_remote_balance))
      sys.exit(1)

    # check that src has enough remote balance
    if src_remote_balance < amt:
      print("ERROR: source channel has {} remote balance, less then what we need to transfer {}".format(src_remote_balance, amt))
      sys.exit(1)

    # check that dst has enough local balance
    if dst_local_balance < amt:
      print("ERROR: destination channel has {} local balance, less then what we need to transfer {}".format(dst_local_balance, amt))
      sys.exit(1)

    dst_chan_id = dst_c["chan_id"]

    capacity = src_c["capacity"]
    chan_id = src_c["chan_id"]

    # Part 1: find route that end for src_remote_pubkey
    max_routes = 20
    print("Querying for up to {} routes".format(max_routes))
    routes = json.loads(subprocess.check_output([
      "lncli", "queryroutes", src_remote_pubkey, str(amt), "--final_cltv_delta", "144", '--num_max_routes', str(max_routes)]
    ).decode("utf-8"))["routes"]
    print("Got {} routes".format(len(routes)))

    indirect_routes = []
    for r in routes:
      if len(r["hops"]) > 1:
        indirect_routes.append(r)

    indirect_routes = sorted(indirect_routes, key=lambda r: len(r["hops"]))

    # Part 2: find route that start from dst_remote_pubkey
    print("All routes: {}".format(len(routes)))

    all_routes = routes
    routes = []
    for r in all_routes:
      if r["hops"][0]["pub_key"] == dst_remote_pubkey:
        routes.append(r)

    print("Filtered routes (only the ones that start with {}): {}".format(dst_remote_pubkey, len(routes)))

    if (len(routes) == 0):
      print("ERROR: no routes found")
      sys.exit(1)

    # pick a route id
    if '--rid' in sys.argv:
      rid = int(sys.argv[sys.argv.index('--rid') + 1])
    else:
      rid = 0
    route = indirect_routes[rid]

    print("-" * 80)
    print("Original route:")
    print_route(route)
    print()

    fee = max(int(x["fee_msat"]) for x in route["hops"])
    #expiry = max(int(x["expiry"]) for x in route["hops"])
    expiry = route["total_time_lock"]
    route["total_time_lock"] += 144

    route = add_self_to_route(route, capacity, chan_id, amt * 1000, fee=(fee * 2), expiry=expiry)
    print("Route after adding self to original route:")
    print_route(route)
    print()

    # TODO:
    #  X update fees and amt_to_forward in all hops
    #  - set expiry on last hop
    #  - call sendtoroute

    print("Total remote balance: {}".format(total_remote_balance))
    answer = input("Going to move {} satoshi to remote balance of {}. Ok (type \"y\")? ".format(amt, dst_chan_id))
    if not answer.startswith("y") and not answer.startswith("Y"):
      sys.exit(1)

    print("Creating invoice for {} sat".format(amt))
    out = subprocess.check_output(["lncli", "addinvoice", "--amt", str(amt), "--expiry", str(3600 * 2)])
    r_hash = json.loads(out.decode("utf-8"))["r_hash"]

    routes = {"routes": [route]}
    routes_json = json.dumps(routes)
    print(routes_json)

    out = subprocess.check_output(["lncli", "sendtoroute", "--pay_hash", r_hash, "--routes", routes_json])
    print("STDOUT: {}".format(out))

  else:
    # TODO: switch to python pretty-table library after documenting an easy way to install the dependency on any platform
    channels = [c for c in channels if c["active"]]
    inactive_channels = [c for c in channels if not c["active"]]

    remote_balance_list = [int(c["remote_balance"]) for c in channels]
    remote_total = sum(remote_balance_list)

    print("Incative channels:")
    print_channels(inactive_channels, remote_total)

    print("\nActive channels:")
    print_channels(channels, remote_total)


    print("\nSuggested new remote balance percentage --dst-pct {:.2f}".format(100 / len(channels)))


if __name__ == "__main__":
  main()
