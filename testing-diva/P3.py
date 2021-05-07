# python3 P3.py [peers]

from setup.setup import download, setup, start_testnet, stop_testnet, delete, API
from utils import *

from pprint import pprint
from time import sleep

import os


def test(peers):

	try:
		results = []
		blocks = []
		last_len_blocks = 1

		download()
		setup(peers)
		is_ready = start_testnet(peers)

		if is_ready:
			print("[*] Stopping peers ...")
			stop_peers(1, peers)
			print("[*] All peers stopped successfully.")
		
		else:
			print("\n[!] TIMEOUT while trying to connect to DIVA.EXCHANGE explorer!")
			print("[*] Test Failed!")
			stop_testnet()
			delete()
				
		# testing cycles
		for i in range(1, peers+1):

			print(f"\n****************************** start test round {i} **************************")

			print(f"[#] Start peer n{i}.")
			start_peer(i)
			
			# wait for a ping
			timeout = 180
			waiting = 0
			no_ping = False

			while len(blocks) <= last_len_blocks or not is_ping(blocks[0]):  # blocks[0] is the newest
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
				print(f"[*] No other ping arrived with {i} peers started!")
				results.append((i, "--no time--", "--no block--", "--no signers--"))

			else:
				print(f"[*] Another ping arrived after {waiting} sec in block nr. {len(blocks)} with {i} peers started.")
				signatures = get_signatures(blocks[0])
				signers = get_signers(blocks[0])
				results.append((i, waiting, len(signatures), signers))
				last_len_blocks = len(blocks)

	except KeyboardInterrupt:
		print("\n[!] Aborting Test! Please wait!")

	except BaseException as e:
		print("\n[!] Unexpected Error!")
		print(str(e))

	finally:
		stop_testnet()
		delete()

	try:
		print(render_results_P3(results))
	
	except BaseException as e:
		print("\n[!] Unexpected Error!")
		print(str(e))
		pprint(results)


if __name__ == "__main__":
	from sys import argv

	if len(argv) > 2:
		peers = int(argv[2])

	else:
		peers = 9    # 3f+1 - 2f+1 = 2
		# peers = 15 # 3f+1 - 2f+1 = 3
	
	print(f"[*] Starting test P2 with {peers} peers")
	test(peers)
