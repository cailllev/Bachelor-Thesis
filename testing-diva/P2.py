# python3 P2.py [all | <peers_count> | <None>]

from setup.setup import download, setup, start_testnet, stop_testnet, delete
from utils import *

from pprint import pprint
from time import time

import os


def test(peers):

	try:
		results = []

		download()
		setup(peers)
		is_ready = start_testnet(peers)
		

		if is_ready:
		
			print("[*] Stopping all peers ... (except API peer n1)")
			stop_peers(2, peers)
			print("[*] All peers stopped successfully.")

			for i in range(1, peers):

				print(f"\n****************************** start test round {i} **************************")

				if i != 1: # API (n1) is always up
					print(f"[*] Starting peer n{i}.")
					start_peer(i)
				
				# 2f+1
				if i <= peers / 2:
					timeout = 60 # not expecting a remove
				else:
					timeout = 15 * 60  # expecting a remove

				to_remove = peers
				print(f"[#] Trying to remove peer n{to_remove} with timeout of {timeout} sec and {i} peers up.")
				start_t = time()
				res = remove_peer(to_remove, timeout)

				if res.status_code == 200:	
						
					block = get_blocks()[0]
					duration = round(time() - start_t)
					try:
						signatures = get_signatures(block)
						signers = get_signers(block)
					except BaseException as e:
						print("[!] Malformed block!\n")
						pprint(block)
						print()
						signatures = 0
						signers = []
					results.append((i, f"n{to_remove}", duration, len(signatures), signers))

					print(f"[*] Peer n{to_remove} successfully removed after {duration} sec with {i} peers up => test complete!")
					break

				else:
					print(f"[*] Could not remove peer n{to_remove} with {i} peers up out of {peers} peers.")
					results.append((i, "--", timeout, "--", "--"))
		
		else:
			print("\n[!] TIMEOUT while trying to connect to DIVA.EXCHANGE explorer!")
			print("[*] Test Failed!")

	except KeyboardInterrupt:
		print("\n[!] Aborting Test! Please wait!")

	except BaseException as e:
		print("\n[!] Unexpected Error!")
		print(str(e))

	finally:
		stop_testnet()
		delete()

	try:
		print(render_results(results, peers, ["peers up", "removed", "after", "signs", "signers"], "P2"))
	
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
				print(f"[*] Starting test P2 with {peers} peers.")
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
