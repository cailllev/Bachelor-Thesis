from setup.setup import download, setup, start_testnet, cleanup, API, EXPLORER
from utils import *

from pprint import pprint
from time import sleep

import requests as req
import json

NODES = 50
BENCHMARK = True

def benchmark():
	download()
	setup(NODES, BENCHMARK)
	start_testnet(BENCHMARK)

	print("\n------------------------------ network up - check ram and cpu usage ----------")
	print("Enter following in separate terminal:")

	 # takes 5 snapshots of top, takes the header of those snapshots and saves them to top_benchmark.txt
	input("$ top -b -n 5 -d 1 | grep \"top - \" -A5 > top_benchmark.txt")

	cleanup()


if __name__ == "__main__":
	benchmark()
