#!/usr/bin/python3
# python3 P3.py

from setup.setup import download, setup, start_testnet, stop_testnet, delete, API
from utils import *

from pprint import pprint
from time import sleep

import os


NODES = 16
results = []

def test():

	try:
		download()
		setup(NODES)
		
		is_ready = start_testnet(NODES)
		if is_ready:
			stop_nodes(1, NODES)
			sleep(15)
			print("[*] All nodes stopped successfully.")
		
		else:
			print("\n[!] TIMEOUT while trying to connect to DIVA.EXCHANGE explorer!")
			print("[*] Test Failed!")
			stop_testnet()
			cleanup()
				
		# testing cycles
		last_blocks_length = 1
		for i in range(1, NODES+1):

			print(f"\n------------------------------ start test round {i} --------------------------")

			print(f"[#] Start node {i}.")
			start_node(i)
			
			# wait for a ping
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

	except KeyboardInterrupt:
		print("\n[!] Aborting Test! Please wait!")

	except BaseException as e:
		print("\n[!] Unexpected Error!")
		print(str(e))

	finally:
		stop_testnet()
		delete()


	print(render_results_P3(results))


if __name__ == "__main__":
	test()
