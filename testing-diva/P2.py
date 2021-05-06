#!/usr/bin/python3
# python3 P3.py

from setup.setup import download, setup, start_testnet, stop_testnet, delete
from utils import *

from pprint import pprint
from time import sleep

import os


def test(nodes):

	try:
		results = []
		blocks = []

		download()
		setup(nodes)
		is_ready = start_testnet(nodes)

		if is_ready:
			stop_nodes(1, nodes)
			sleep(15)
			print("[*] All nodes stopped successfully.")
		
		else:
			print("\n[!] TIMEOUT while trying to connect to DIVA.EXCHANGE explorer!")
			print("[*] Test Failed!")
			stop_testnet()
			delete()

		# next peer to remove
		to_remove = nodes
		last_remove_successful = False
		started_nodes = 0
				
		# testing cycles
		for i in range(1, nodes+1):

			print(f"\n------------------------------ start test round {i} --------------------------")

			# only start the node, if no success at removing peer
			if not last_remove_successful:
				print(f"[#] Start peer n{i} ...")
				start_node(i)
				started_nodes += 1

			if started_nodes == to_remove:
				print("[*] Last started node == next node to remove. Test complete.")
				break
			
			# try if remove peer already works (always test the last)
			last_remove_successful = True
			remove_peer(to_remove)

			timeout = 180
			waiting = 0

			while len(get_peers()) == to_remove:  # wait until on peer was removed
				blocks = get_blocks()

				# only print every 10 sec
				if waiting % 10 == 0:
					print(f"[#] Wait for another ping, waited for {waiting} sec ...")

				if waiting >= timeout:
					last_remove_successful = False
					break
				
				waiting += 1
				sleep(1)

			if last_remove_successful:
				print(f"[*] Peer n{to_remove} successfully removed with {started_nodes} started peers.")	
				to_remove -= 1

				signatures = get_signatures(blocks[0])
				signers = get_signers(blocks[0])
				results.append((started_nodes, waiting, len(signatures), signers))

			else:
				print(f"[*] Could not remove peer n{to_remove}.")
				results.append((started_nodes, "--no time--", "--no block--", "--no signers--"))


	except KeyboardInterrupt:
		print("\n[!] Aborting Test! Please wait!")

	except BaseException as e:
		print("\n[!] Unexpected Error!")
		print(str(e))

	finally:
		stop_testnet()
		delete()

	try:
		print(render_results_P2(results))
	
	except BaseException as e:
		print("\n[!] Unexpected Error!")
		print(str(e))
		pprint(results)


if __name__ == "__main__":
	from sys import argv

	if len(argv) > 2:
		nodes = int(argv[2])

	else:
		nodes = 16
	
	test(nodes)
