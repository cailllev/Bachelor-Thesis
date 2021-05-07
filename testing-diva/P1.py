# python3 P1.py [peers]


from setup.setup import download, setup, start_testnet, stop_testnet, delete, API
from utils import *

from pprint import pprint
from time import sleep
from sys import stdout

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
				
			waiting = 0

			while len(blocks) <= last_len_blocks or not is_ping(blocks[0]):  # blocks[0] is always the newest block
				if waiting % 10 == 0:
					print(f"[#] Wait for first ping, waited for {waiting} sec ...")					

				blocks = get_blocks()
				waiting += 1
				sleep(1)
			
			# first ping arrived, start test (i.e. stop peers one after another)
			print(f"[*] Got first ping in block nr. {len(blocks)} after {waiting} sec.")
			last_len_blocks = len(blocks)

			for i in range(peers, 0, -1): # n16, n15, ..., n1
			
				stopped_peers = peers + 1 - i
				
				print(f"\n****************************** start test round {i} **************************")

				print(f"[*] Stopping peer n{i}.")
				stop_peer(i)

				# now wait for next ping, expected arrival between 60 and 120 sec after previous ping
				timeout = 1800  # 30 mins to include safety buffer
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
					print(f"[*] No other ping arrived with {stopped_peers} peers stopped!")
					results.append((stopped_peers, "--no ping--", "--no block--", "--no ping--"))

				else:
					print(f"[*] Another ping arrived after {waiting} sec in block nr. {len(blocks)} with {stopped_peers} peers stopped.")
					signatures = get_signatures(blocks[0])
					signers = get_signers(blocks[0])
					results.append((stopped_peers, waiting, len(signatures), signers))
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
	from sys import argv

	if len(argv) > 2:
		peers = int(argv[2])

	else:
		peers = 9    # 3f+1 - 2f+1 = 2
		# peers = 15 # 3f+1 - 2f+1 = 3
	
	print(f"[*] Starting test P2 with {peers} peers")
	test(peers)
