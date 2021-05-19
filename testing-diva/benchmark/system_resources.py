# cp benchmark/system_resources.py . && python3 system_resources.py; rm system_resources.py
# -> has to be run from inside testing-diva folder

from setup.setup import download, setup, start_testnet, stop_testnet, delete, API, EXPLORER

NODES = 50
BENCHMARK = True

def benchmark():
	download()
	setup(NODES, BENCHMARK)
	start_testnet(NODES, BENCHMARK)

	print("\n------------------------------ network up - check ram and cpu usage ----------")
	print("Enter following in separate terminal:")

	 # takes 100 snapshots of top, takes the header of those snapshots and saves them to benchmark/system_resources_results.txt
	input("$ top -b -n 100 -d 1 | grep \"top - \" -A5 > benchmark/system_resources_results.txt")

	stop_testnet()
	delete()


if __name__ == "__main__":
	benchmark()
