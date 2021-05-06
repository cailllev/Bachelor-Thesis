#!/usr/bin/python3
# python3 P1.py


from setup.setup import download, setup, start_testnet, stop_testnet, delete, API
from utils import *

from pprint import pprint
from time import sleep
from sys import stdout

import os


NODES = 16


def test():

	try:
		results = []
		last_len_blocks = 1
		blocks = []

		download()
		setup(NODES)
		is_ready = start_testnet(NODES)

		if is_ready:
				
			waiting = 0

			while len(blocks) <= last_len_blocks or not is_ping(blocks[0]):  # blocks[0] is always the newest block
				if waiting % 5 == 0:
					print(f"[#] Wait for first ping, waited for {waiting} sec ...")					

				blocks = get_blocks()
				waiting += 1
				sleep(1)
			
			# first ping arrived, start test (i.e. stop nodes one after another)
			print(f"[*] Got first ping in block nr. {len(blocks)}")
			last_len_blocks = len(blocks)

			for i in range(NODES, 0, -1): # n16, n15, ..., n1
			
				stopped_nodes = NODES + 1 - i
				
				print(f"\n------------------------------ start test round {i} --------------------------")

				print(f"[*] Stop node n{i} ...")
				stop_node(i)

				# now wait for next ping, expected arrival between 60 and 120 sec after previous ping
				timeout = 180
				waiting = 0
				no_ping = False

				while len(blocks) <= last_len_blocks or not is_ping(blocks[0]):
					blocks = get_blocks()

					# only print every 10 sec
					if waiting % 10 == 0:
						print(f"[#] Wait for another ping, waited for {waiting} sec ...")

					if waiting >= timeout:
						no_ping = True
						break
					
					waiting += 1
					sleep(1)

				if no_ping:
					print(f"[*] No other ping arrived with {stopped_nodes} node(s) stopped!")
					results.append((stopped_nodes, "--no time--", "--no ping--", "--no signers--"))

				else:
					print(f"[*] Another ping arrived after {waiting} sec in block nr. {len(blocks)} with {stopped_nodes} node(s) stopped.")
					signatures = get_signatures(blocks[0])
					signers = get_signers(blocks[0])
					results.append((stopped_nodes, waiting, len(signatures), signers))
					last_len_blocks = len(blocks)


		else:
			print("\n[!] TIMEOUT while trying to connect to Iroha Blockchain Explorer!")
			print("[!] Test Failed!")

	except KeyboardInterrupt:
		print("\n[!] Aborting Test! Please wait!")

	except BaseException as e:
		print("\n[!] Unexpected Error!")
		print(str(e))

	finally:
		stop_testnet()
		delete()

	try:
		print(render_results_P1(results))
	
	except BaseException as e:
		print("\n[!] Unexpected Error!")
		print(str(e))
		pprint(results)

if __name__ == "__main__":
	test()
