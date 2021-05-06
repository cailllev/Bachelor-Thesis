# python3 P2.py [peers]

from setup.setup import download, setup, start_testnet, stop_testnet, delete
from utils import *

from pprint import pprint

import os


def test(peers):

	try:
		results = []

		download()
		
		# testing cycles, stop all except:
		# n1; 
		# n1,n2;
		# ...
		# ...
		# n1,n2,n3,...,peers;
		for i in range(1, peers+1):

			setup(peers)
			is_ready = start_testnet(peers)

			if is_ready:

				print(f"\n------------------------------ start test round {i} --------------------------")
			
				to_remove = peers # start with (trying to) remove n16

				# stop all peers that are not in current cycle
				print(f"[*] Stopping peers n{i+1} ... n{peers}.")
				stop_peers(i+1, peers)

				while True:
				
					# try to remove peer (always test the last)
					res = remove_peer(to_remove, 120)

					if res.status_code == 200:	
						
						to_remove -= 1
						block = get_blocks()[0]

						signatures = get_signatures(block)
						signers = get_signers(block)
						results.append((i, to_remove, len(signatures), signers))
						
						still_up = min(i, to_remove)
						print(f"[*] Peer n{to_remove} successfully removed with {still_up} started peers.")

						if to_remove == 1:
							print(f"[*] Removed peers except n1 => test round complete.")
							break

					else:
						print(f"[*] Could not remove peer n{to_remove} with {i} started peers => test round complete.")
						results.append((i, "--no one--", "--no block--", "--no signers--"))
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
		peers = int(argv[2])

	else:
		peers = 9    # 3f+1 - 2f+1 = 2
		# peers = 15 # 3f+1 - 2f+1 = 3
	
	print(f"[*] Starting test P2 with {peers} peers")
	test(peers)
