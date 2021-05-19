# cp benchmark/remove.py . && python3 remove.py 9; rm remove.py
# -> has to be run from inside testing-diva folder

from setup.setup import download, setup, start_testnet, stop_testnet, delete
from utils import *

from pprint import pprint
from time import time

import os


def test(peers):

	try:
		download()
		setup(peers)
		is_ready = start_testnet(peers)
		
		if is_ready:
			to_remove = peers
			timeout = 15*60

			print(f"[#] Trying to remove peer n{to_remove} with timeout of {timeout} sec and {peers} peers up.")

			start_t = time()
			res = remove_peer(to_remove, timeout)

			if res.status_code == 200:	
				
				duration = round(time() - start_t)	

				block = get_blocks()[0]
				signatures = get_signatures(block)
				signers = get_signers(block)

				print(f"[*] Peer successfully removed => benchmark complete!")
				print("\n------------------------------ results ---------------------------------------")
				print(f"[#] Peers up:      {peers} peers")
				print(f"[#] Peer removed:  n{to_remove}")
				print(f"[#] After:         {duration} sec")
				print(f"[#] Signs:         {len(signatures)} signatures")
				print(f"[#] Signers:       {', '.join(signers)}")

			else:
				print(f"[!] Could not remove peer!")
		
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


if __name__ == "__main__":
	from sys import argv
	
	if len(argv) > 1:

		# test given peers count
		peers = int(argv[1])
		test(peers)

	# test default peers count
	else:
		peers = 9
		test(peers)
