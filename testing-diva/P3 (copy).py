from setup.setup import download, setup, start_testnet, stop_testnet, delete, API, EXPLORER
from utils import *

from pprint import pprint
from time import sleep
from sys import stdout

import requests as req
import json
import os


NODES = 10
success = []
no_success = []


def test():
	download()
	setup(NODES)

	for i in range(1, 51):

		is_ready = start_testnet()
		if is_ready:
			
			print(f"\n------------------------------ network up - start test round {i} -------------")
			blocks = []
			while len(blocks) < 2:
				res = req.get(f"{EXPLORER}/blocks")
				blocks = json.loads(res.text)["blocks"]
				print("[#] Waiting for first ping...")
				sleep(5)

			# first ping arrived
			signatures_count_1 = len(get_signatures(blocks[0]))

			# wait for 50 sec, then stop the containers
			for t in range(50, 0, -1):
				stdout.write("\r[#] Got first ping, sleep for %2d sec" % (t))
				stdout.flush()
				sleep(1)

			stdout.write("\n")
			print("[#] Stop docker containers...")

			names = ""
			for j in range(i):
				names += f"n{j+1}.testnet.diva.local n{j+1}.db.testnet.diva.local"
				
			os.system(f"sudo docker stop {names}") # --remove-orphans

			# now wait for 2nd ping
			timeout = 60
			waiting = 0
			while waiting < timeout:
				res = req.get(f"{EXPLORER}/blocks")
				blocks = json.loads(res.text)["blocks"]
				pprint(blocks)
				
				# ping arrived?
				if len(blocks) == 3:
					print(f"[*] SUCCESS WITH {i} NODES STOPPED!")
					signatures_count_2 = len(get_signatures(blocks[0]))
					success.append((i, signatures_count_1, signatures_count_2))
					break

				print("[#] Waiting for second ping...")
				waiting += 5
				sleep(5)

			else:
				print(f"NO SUCCESS WITH {i} NODES STOPPED!")
				no_success.append((i, signatures_count_1))

			stop_testnet()

		else:
			print("\n[!] TIMEOUT while trying to connect to DIVA.EXCHANGE explorer!")
			print("[*] TESTS FAILED!")
			stop_testnet()
			break

	delete()

	print("\n[*] RESULTS!")
	pprint(success)
	pprint(no_success)


if __name__ == "__main__":
	test()
