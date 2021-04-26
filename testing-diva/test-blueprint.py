from setup.setup import download, setup, start_testnet, stop_testnet, delete, API, EXPLORER
from utils import *

from pprint import pprint
from time import sleep

import requests as req
import json

NODES = 7

# inspect logs: sudo docker logs n1.testnet.diva.local
# inspect code at runtime: code.interact(local=dict(globals(), **locals()))


def test():
	download()
	setup(NODES)

	is_ready = start_testnet()
	if is_ready:

		print("\n------------------------------ network up - start tests ----------------------")

		blocks = []
		while len(blocks) < 2:
			res = req.get(f"{EXPLORER}/blocks")
			blocks = json.loads(res.text)["blocks"]
			print("[#] Waiting for next block...")
			sleep(5)

		print("\n[*] ping committed to blockchain")
		
		# newest block is at the start [0]
		print("   - block number:".ljust(25), get_block_number(blocks[0]))

		print("   - block id:".ljust(25), get_id(blocks[0]))

		print("   - creation date:".ljust(25), get_creation_date(blocks[0]))
		
		print("   - transactions count:".ljust(25), get_transactions_count(blocks[0]))

		print("   - signatures:")
		pprint(get_signatures(blocks[0]))

		print("\n[*] ALL TESTS PASSED!")


	else:
		print("\n[!] TIMEOUT while trying to connect to DIVA.EXCHANGE explorer!")
		print("[*] TESTS FAILED!")

	stop_testnet()
	delete()


if __name__ == "__main__":
	test()