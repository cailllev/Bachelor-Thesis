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

			print(f"\n------------------------------ network up - start test round {i} -------------")

			print(f"[#] Start node {i}.")
			start_node(i)
			
			# wait for 120 sec for a ping
			timeout = 120
			waiting = 0
			while waiting < timeout:
				blocks = get_blocks()
				
				# ping arrived?
				if len(blocks) == last_blocks_length + 1:
					print(f"[*] New ping arrived with {i} nodes started.")
					signatures_count = len(get_signatures(blocks[0]))
					results.append((i, signatures_count))
					break

				print(f"[#] No new ping, waited for {waiting} sec...")
				waiting += 5
				sleep(5)

			# no ping arrived
			else:
				print(f"[*] No new ping arrived with {i} nodes started.")
				results.append((i, "--no ping--"))
				
			last_blocks_length = len(blocks)

			# start and stop all other nodes, circumvent timeout
			# i+2, because i+1 gets started in next loop
			if i+2 <= NODES:
				print("[*] Start and stop remaining nodes.")
				start_nodes(i + 2, NODES)
				sleep(30) # wait for all started before stopping again
				stop_nodes(i + 2, NODES)


		stop_testnet()
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

	print(render_results_P3(results))


if __name__ == "__main__":
	test()
