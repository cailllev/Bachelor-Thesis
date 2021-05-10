# python3 P3.py [all | <peers_count> | <None>]

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
			print("[*] Stopping all peers ... (except API peer n1)")
			stop_peers(2, peers)
			print("[*] All peers stopped successfully.")
				
			# testing cycles
			for i in range(1, peers+1):

				print(f"\n****************************** start test round {i} **************************")

				if i != 1: # API (n1) is always up
					print(f"[*] Starting peer n{i}.")
					start_peer(i)

				# 2f+1
				if i <= peers / 2:
					timeout = 60 # not expecting a ping
				else:
					timeout = 15 * 60  # expecting a ping

				waiting = 0
				no_ping = False

				# now wait for next ping
				while len(blocks) <= last_len_blocks or not is_ping(blocks[0]):  # blocks[0] is the newest
					blocks = get_blocks()
					
					print(f"\r[#] Wait for another ping, waited for {waiting} sec ...", end="")

					if waiting >= timeout:
						no_ping = True
						break
					
					waiting += 1
					sleep_till_whole_sec()


				if no_ping:
					print(f"\r[*] No other ping arrived after {waiting} sec with {i} peers up out of {peers} peers.")
					results.append((i, waiting, "--", "--"))

				else:
					print(f"\r[*] Another ping arrived after {waiting} sec in block nr. {len(blocks)} with {i} peers up out of {peers} peers")
					signatures = get_signatures(blocks[0])
					signers = get_signers(blocks[0])
					results.append((i, waiting, len(signatures), signers))
					last_len_blocks = len(blocks)

		else:
			print("\n[!] TIMEOUT while trying to connect to DIVA.EXCHANGE explorer!")
			print("[*] Test Failed!")
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
		print(render_results(results, peers, ["peers up", "ping at", "signs", "signers"], "P3"))
	
	except BaseException as e:
		print("\n[!] Unexpected Error!")
		print(str(e))
		pprint(results)


if __name__ == "__main__":
	from sys import argv
	optimalPeers = [9, 15, 21, 27, 33] # see 2f_3f_optimal.diff
	
	if len(argv) > 1:

		# test all?
		if argv[1] in ["All", "all", "A", "a"]:
			for peers in optimalPeers:
				print("******************************************************************************")
				print(f"[*] Starting test P3 with {peers} peers.")
				print("******************************************************************************")
				test(peers)

		# test given peers count
		else:
			peers = int(argv[1])
			test(peers)

	# test default peers count
	else:
		peers = 9
		test(peers)
