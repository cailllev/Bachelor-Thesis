from setup.setup import download, setup, start_testnet, cleanup, API, EXPLORER

import requests as req

NODES = 7

def test():
	download()
	setup(NODES)

	is_ready = start_testnet()
	if is_ready:
		res = req.get(EXPLORER)
		blockchain_data = res.text
		print(blockchain_data)

	else:
		raise Exception("[!] TIMEOUT while trying to connect to DIVA.EXCHANGE explorer!")


if __name__ == "__main__":
	test()