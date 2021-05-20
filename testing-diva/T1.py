# python3 T1.py [all | <peers_count> | <None>]
# -> has to be run from inside testing-diva folder

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

			print(f"\n****************************** start test round 0 **************************")

			while len(blocks) <= last_len_blocks or not is_ping(blocks[0]):  # blocks[0] is always the newest block
				print(f"\r[#] Wait for first ping, waited for {waiting} sec ...", end="")					

				blocks = get_blocks()
				waiting += 1
				sleep_till_whole_sec()
			
			# first ping arrived, start test (i.e. stop peers one after another)
			print(f"\n[*] Got first ping in block nr. {len(blocks)} after {waiting} sec.")
			last_len_blocks = len(blocks)

			signatures = get_signatures(blocks[0])
			signers = get_signers(blocks[0])
			results.append((peers, waiting, len(signatures), signers))

			for i in range(peers, 0, -1): # n9, n8, ..., n1
			
				stopped_peers = peers + 1 - i
				running_peers = i-1
				
				print(f"\n****************************** start test round {stopped_peers} **************************")

				print(f"[*] Stopping peer n{i}.")
				stop_peer(i)

				# 2f+1
				if running_peers <= peers / 2:
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
					print(f"\r[*] No other ping arrived after {waiting} sec with {running_peers} peers up out of {peers} peers.")
					results.append((running_peers, waiting, "--", "--"))

				else:
					print(f"\r[*] Another ping arrived after {waiting} sec in block nr. {len(blocks)} with {running_peers} peers up out of {peers} peers.")
					signatures = get_signatures(blocks[0])
					signers = get_signers(blocks[0])
					results.append((running_peers, waiting, len(signatures), signers))
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
		print(render_results(results, peers, ["peers up", "ping at", "signs",  "signers"], "T1"))
	
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
				print(f"[*] Starting test T1 with {peers} peers.")
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
	
