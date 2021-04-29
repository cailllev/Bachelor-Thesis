from setup.setup import download, setup, start_testnet, stop_testnet, delete, API, EXPLORER
from utils import *

from pprint import pprint
from time import sleep
from sys import stdout
from threading import Thread

import requests as req
import json
import os


NODES = 16
success = []
no_success = []


def stop_node(n):
	names = f"n{y}.testnet.diva.local n{y}.db.testnet.diva.local"
	print("[#] Stopping: ", names)
	os.system(f"sudo docker stop {names}")


def test():

	try:
		download()
		setup(NODES)
		
		#Stopps all nodes if ready
		is_ready = start_testnet()
		if is_ready:
			for n in range (1, NODES+1):
				t = Thread(target=stop_node, args=(n,))
				t.start()
				t.join()

			print("[*] All nodes stopped successfully.")
		
		else:
			print("\n[!] TIMEOUT while trying to connect to DIVA.EXCHANGE explorer!")
			print("[*] TESTS FAILED!")
			stop_testnet()
			cleanup()
			exit(1)
				
		# testing cycles.
		last_blocks_length = 1
		for i in range(1, NODES+1):

			print(f"\n------------------------------ network up - start test round {i} -------------")

			# start node
			print(f"[#] start node {i}")
			os.system(f"sudo docker start n{i}.testnet.diva.local n{i}.db.testnet.diva.local")
			
			# wait for 60 sec for a ping.
			for t in range(60, 0, -1):
				res = req.get(f"{EXPLORER}/blocks")
				blocks = json.loads(res.text)["blocks"]
				stdout.write("\r[#] Waiting for first ping, sleep for %2d sec" % (t))
				stdout.flush()
				sleep(1)
			stdout.write("\n")
				
			# handle ping
			if len(blocks) == last_blocks_length + 1:
				success.append(i)
			elif len(blocks) == last_blocks_length:
				no_success.append(i)
			else:
				print("[!] Strange blockchain!")
				pprint(blocks)
			last_blocks_length = len(blocks)


		stop_testnet()
		delete()

	except KeyboardInterrupt:
		print("\n[!] Aborting Test!")
		stop_testnet()
		delete()

	except BaseException:
		print("\n[!] Unexpected Error!")
		stop_testnet()
		delete()

	print("\n------------------------------ results ---------------------------------------")
	print("[*] Pings arrived at:")
	pprint(success)
	print("\n[*] No pings arrived at:")
	pprint(no_success)


if __name__ == "__main__":
	test()
