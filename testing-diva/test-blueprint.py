from setup.setup import download, setup, start_testnet, cleanup, API, EXPLORER
from pprint import pprint
from time import sleep

import requests as req
import json

NODES = 7

def test():
	download()
	setup(NODES)

	is_ready = start_testnet()
	if is_ready:
		res = req.get(f"{EXPLORER}/blocks")
		blocks = json.loads(res.text)["blocks"]

		pprint(blocks[-1])
		input("wait...")

		# instead of print(block) and input(), do some tests

		# create new block?
		# req.post("...diva-api/.../new block...", data="...")

		# blocks[0] => first block
		# blocks[-1] => last block

		# iterate through all blocks
		# for block in blocks:
		#	 pprint(block)
		#	 ...

	else:
		print("[!] TIMEOUT while trying to connect to DIVA.EXCHANGE explorer!")

	cleanup()


if __name__ == "__main__":
	test()