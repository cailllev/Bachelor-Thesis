# cp benchmark/system_resources.py . && python3 system_resources.py 50; rm system_resources.py
# -> has to be run from inside testing-diva folder

from setup.setup import download, setup, start_testnet, stop_testnet, delete, API, EXPLORER

from threading import Thread
from os import system
from sys import argv


# Total reclaimed space: 2.47GB (with 50 nodes)


def top():
	system("top -b -n 100 -d 1 | grep \"top - \" -A5 > benchmark/system_resources_results.txt")


def benchmark(nodes):
	try:
		download()
		
		print("\n------------------------------ download complete - start checking usage ------")
		t = Thread(target=top, args=())
		t.start()
		
		setup(nodes, benchmark=True)
		start_testnet(nodes, benchmark=True)

		print("\n------------------------------ all started, wait for top to finish -----------")
		t.join()

	except KeyboardInterrupt:
		print("\n[!] Aborting! Please wait.")

	finally:
		stop_testnet()
		delete()		


if __name__ == "__main__":

	if len(argv) > 1:
		nodes = int(argv[1])

	else:
		nodes = 50 # default

	benchmark(nodes)
