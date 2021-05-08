# python3 P2.py [all | <peers_count> | <None>]

from setup.setup import download, setup, start_testnet, stop_testnet, delete
from utils import *

from pprint import pprint

import os


def test(peers, exhaustive):

	try:
		results = []

		download()
		setup(peers)
		is_ready = start_testnet(peers)
		

		if is_ready:
		
			# testing cycles, stop all except:
			# n1; 
			# n1,n2;
			# ...
			# ...
			# n1,n2,n3,...,peers-1;
			for i in range(1, peers):

				print(f"\n****************************** start test round {i} **************************")

				to_remove = peers # start with (trying to) remove last peer
				removed_peers = []
				timeout = 60

				# stop all peers that are not in current cycle
				print(f"[*] Stopping peers n{i+1} ... n{peers}.")
				stop_peers(i+1, peers)

				while True:
				
					# try to remove peer (always the last first)
					res = remove_peer(to_remove, timeout)

					if res.status_code == 200:	
						
						block = get_blocks()[0]
						try:
							signatures = get_signatures(block)
							signers = get_signers(block)
						except BaseException as e:
							print("[!] Malformed block!\n")
							pprint(block)
							print()
							signatures = 0
							signers = []
						results.append((i, to_remove, len(signatures), signers))

						removed_peers.append(to_remove)						
						to_remove -= 1
						
						still_up = min(i, to_remove+1)
						print(f"[*] Peer n{to_remove+1} successfully removed with {still_up} peers up.")

						if not exhaustive:
							print(f"[*] Non exhaustive mode => test round complete.")
							break


						if to_remove == 1:
							print(f"[*] Removed all peers except n1 => test round complete.")
							break

					else:
						print(f"[*] Could not remove peer n{to_remove} with {i} peers up out of {peers} peers => test round complete.")
						results.append((i, to_remove, "--still up--", "--"))
						break


				# start all nodes and add all removed peers
				print(f"[*] Starting peers n{i+1} ... n{peers} again.")
				start_peers(i+1, peers)

				for peer in removed_peers:
					add_peer(peer, timeout)

					# TODO: check if really removed, otherwise clean delete and setup!

		
		else:
			print("\n[!] TIMEOUT while trying to connect to DIVA.EXCHANGE explorer!")
			print("[*] Test Failed!")
			break

	except KeyboardInterrupt:
		print("\n[!] Aborting Test! Please wait!")

	except BaseException as e:
		print("\n[!] Unexpected Error!")
		print(str(e))

	finally:
		stop_testnet()
		delete()

	try:
		print(render_results(results, peers, ["peers up", "removed peer", "signs on remove", "signers"], "P2"))
	
	except BaseException as e:
		print("\n[!] Unexpected Error!")
		print(str(e))
		pprint(results)


if __name__ == "__main__":
	from sys import argv
	optimalPeers = [9, 15, 21, 27, 33] # see 2f_3f_optimal.diff
	exhaustive = False # after successful removal of peer ni, remove ni-1, ni-2, ... n2
	
	if len(argv) > 1:

		# test all?
		if argv[1] in ["All", "all", "A", "a"]:
			for peers in optimalPeers:
				print("******************************************************************************")
				print(f"[*] Starting test P2 with {peers} peers.")
				print("******************************************************************************")
				test(peers, exhaustive)

		# test given peers count
		else:
			peers = int(argv[1])
			test(peers, exhaustive)

	# test default peers count
	else:
		peers = 9
		test(peers, exhaustive=True)
