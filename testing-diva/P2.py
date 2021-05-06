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

		download()
		
		# testing cycles
		for i in range(1, nodes+1):

			setup(nodes)
			is_ready = start_testnet(nodes)
			to_remove = nodes

			if is_ready:

				print(f"\n------------------------------ start test round {i} --------------------------")

				# stop all nodes that are not in current cycle
				print(f"[*] Stopping peers n{i+1} ... n{nodes} ...")
				stop_nodes(i+1, nodes)
				sleep(20)
				print("[*] Peers stopped successfully.")

				while True:
				
					# try to remove peer (always test the last)
					res = remove_peer(to_remove)

					if res.status_code == 200:
						to_remove -= 1

						block = get_blocks()[0]
						pub_key = json.loads(res.text)["publicKey"]
						
						if is_remove_peer(block, pub_key):
							print(f"[*] Peer n{to_remove} successfully removed with {i} started peers.")	

							signatures = get_signatures(block)
							signers = get_signers(block)
							results.append((i, to_remove, len(signatures), signers))

						else:
							print(f"[!] Removed peer n{to_remove} but no entry in blockchain found!")
							results.append((i, to_remove, "--no block--", "--no signers--"))

						if to_remove == i:
							print(f"[*] Removed all non started peers (n{nodes} ... n{i+1}) => test round complete.")
							break

					else:
						print(f"[*] Could not remove peer n{to_remove} with {i} started peers => test round complete.")
						results.append((i, "--not removed--", "--no block--", "--no signers--"))
						break
		
			else:
				print("\n[!] TIMEOUT while trying to connect to DIVA.EXCHANGE explorer!")
				print("[*] Test Failed!")
				break

			stop_testnet()
			delete()


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
