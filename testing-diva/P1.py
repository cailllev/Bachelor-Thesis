from setup.setup import download, setup, start_testnet, stop_testnet, delete, API
from utils import *

from pprint import pprint
from time import sleep
from sys import stdout

import os


NODES = 16
results = []


def test():

	try:
		download()
		setup(NODES)

		for i in range(NODES, 0, -1): # n16, n15, ..., n1

			is_ready = start_testnet()
			if is_ready:
				stopped_nodes = NODES + 1 - i
				
				print(f"\n------------------------------ network up - test {stopped_nodes} stopped node(s) -----------")
				blocks = []
				waiting = 0
				while len(blocks) < 2:
					blocks = get_blocks()
					print(f"[#] No 1st ping, waited for {str(waiting).rjust(2)} sec...")
					waiting += 5
					sleep(5)

				# first ping arrived
				signatures_count_1 = len(get_signatures(blocks[0]))

				# wait for 45 sec, then stop the containers
				for t in range(44, -1, -1):
					sleep(1)
					stdout.write("\r[*] Got first ping, sleep for %2d sec" % (t))
					stdout.flush()

				stdout.write("\n")
				print(f"[*] Stop nodes n{NODES}...n{i}.")
				stop_nodes(i, NODES)

				# now wait for 2nd ping, expected arrival between 60 and 120 sec after first ping
				timeout = 60 + 15
				waiting = 0
				while waiting < timeout:
					blocks = get_blocks()
					
					# ping arrived?
					if len(blocks) == 3:
						print(f"[*] 2nd ping arrived with {stopped_nodes} node(s) stopped.")
						signatures_count_2 = len(get_signatures(blocks[0]))
						results.append((stopped_nodes, signatures_count_1, signatures_count_2))
						break

					# wait for all docker stop messages before printing
					if waiting >= 15:
						print(f"[#] No 2nd ping, waited for {waiting} sec...")
					
					waiting += 5
					sleep(5)

				else:
					print(f"[*] No 2nd ping arrived with {stopped_nodes} node(s) stopped!")
					results.append((stopped_nodes, signatures_count_1, "--no ping--"))

				stop_testnet()

			else:
				print("\n[!] TIMEOUT while trying to connect to DIVA.EXCHANGE explorer!")
				print("[!] Test Failed!")
				stop_testnet()
				break

		delete()

	except KeyboardInterrupt:
		print("\n[!] Aborting Test! Please wait!")
		stop_testnet()
		delete()

	except BaseException as e:
		print("\n[!] Unexpected Error!")
		print(str(e))
		stop_testnet()
		delete()

	print(render_results_P1(results))

if __name__ == "__main__":
	test()