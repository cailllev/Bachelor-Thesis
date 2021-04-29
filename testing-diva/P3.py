from setup.setup import download, setup, start_testnet, stop_testnet, delete, API
from utils import *

from pprint import pprint
from time import sleep
from sys import stdout

import os


NODES = 16
results = []

def test():

	try:
		download()
		setup(NODES)
		
		#Stopps all nodes if ready
		is_ready = start_testnet()
		if is_ready:
			stop_nodes(1, NODES)
			sleep(15)
			print("[*] All nodes stopped successfully.")
		
		else:
			print("\n[!] TIMEOUT while trying to connect to DIVA.EXCHANGE explorer!")
			print("[*] Test Failed!")
			stop_testnet()
			cleanup()
				
		# testing cycles.
		last_blocks_length = 1
		for i in range(1, NODES+1):

			print(f"\n------------------------------ network up - start test round {i} -------------")

			# start node i
			print(f"[#] Start node {i}.")
			os.system(f"sudo docker start n{i}.testnet.diva.local n{i}.db.testnet.diva.local")
			
			# wait for 120 sec for a ping
			timeout = 120
			waiting = 0
			while waiting < timeout:
				blocks = get_blocks()
				
				# ping arrived?
				if len(blocks) == last_blocks_length + 1:
					print(f"[*] New ping arrived with {i} nodes started.")
					signatures_count = len(get_signatures(blocks[0]))
					results.append((i, signatures_count))
					break

				print(f"[#] No new ping, waited for {waiting} sec...")
				waiting += 5
				sleep(5)

			# no ping arrived
			else:
				print(f"[*] No new ping arrived with {i} nodes started.")
				results.append((i, "--no ping--"))
				
			last_blocks_length = len(blocks)


		stop_testnet()
		delete()

	except KeyboardInterrupt:
		print("\n[!] Aborting Test!")
		stop_testnet()
		delete()

	except BaseException as e:
		print("\n[!] Unexpected Error!")
		print(str(e))
		stop_testnet()
		delete()

	print(render_results(results))


if __name__ == "__main__":
	test()
