#!/usr/bin/python3
import os
import sys
import requests as req

from time import sleep
from pathlib import Path

# normal usage from parent dir
try:
	from setup.combine_texts import *

# direct usage from current dir
except ModuleNotFoundError:
	from combine_texts import *

root_path = Path(__file__).parent / ".."
diva_path = Path(__file__).parent / "../diva-dockerized/"

TIMEOUT = 60  # sec
API = "http://172.29.101.30:19012"
EXPLORER = "http://172.29.101.100:3920"


def download():
	print("\n------------------------------ docker diva volumes down ----------------------")
	file = f"{diva_path}/docker-compose/local-testnet.yml"
	if os.path.isfile(file):
		os.system(f"sudo docker-compose -f {file} down --volumes")
	else:
		print("No yml file detected to down the docker volumes.")

	print("\n------------------------------ remove old git --------------------------------")
	os.system(f"rm -rf {diva_path}")
	print("Done.")

	print("\n------------------------------ clone repo ------------------------------------")
	os.system(f"cd {root_path} && git clone -b develop https://codeberg.org/diva.exchange/diva-dockerized.git")
	
	print("\n------------------------------ pull docker images ----------------------------")
	os.system(f"sudo docker-compose -f {root_path}/setup/docker_images_pull.yml pull")


def setup(nodes, benchmark=False):

	# create and write yml file (controls nodes and dbs)
	print("\n------------------------------ adapt yml file --------------------------------")
	print("Changing yml file to create local-testnet with " + str(nodes) + " nodes.")
	yaml_content = combine(nodes, benchmark)
	
	if yaml_content == None:  # i.e. nodes over threshold and not continued and not in benchmark
		cleanup()


	yaml_name = f"{diva_path}/docker-compose/local-testnet.yml"

	with open(yaml_name, "w") as f:
		f.write(yaml_content)


def start_testnet(benchmark=False):
	
	print("\n------------------------------ start testnet ---------------------------------")
	os.system(f"sudo docker-compose -f {diva_path}/docker-compose/local-testnet.yml up -d --remove-orphans")
	
	# all nodes up, return true without explorer and api started
	if benchmark:
		return True

	print("\n------------------------------ test connection -------------------------------")
	print("[*] Testnet is up and running, sending test-request to diva-api/about and explorer.")

	api_responsive = False
	explorer_responsive = False
	time = 0

	while not api_responsive or not explorer_responsive:
		ok_response = True
		api_res_code = None
		exporer_res_code = None

		if time > TIMEOUT:
			return False

		try:
			if not api_responsive:
				res = req.get(API + "/about")
				if res.status_code == 200:
					print("[*] Got 200 response from API.")
					api_responsive = True
				else:
					ok_response = False

			if not explorer_responsive:
				res = req.get(EXPLORER + "/blocks")
				if res.status_code == 200:
					print("[*] Got 200 response from Explorer.")
					explorer_responsive = True
				else:
					ok_response = False
		
		except req.exceptions.RequestException:
			print("[#] No connection, wait for 3 sec...")
			time += 3
			sleep(3)

		if not ok_response:
			print(f"[#] Connected, but res not 200 yet. API: {api_res_code}, Explorer: {exporer_res_code}, wait for 3 sec...")
			time += 3
			sleep(3)

	return True


def stop_testnet():
	print("\n------------------------------ docker diva volumes down ----------------------")
	os.system(f"sudo docker-compose -f {diva_path}/docker-compose/local-testnet.yml down --volumes")
	os.system(f"sudo docker volume prune -f")


def delete():
	print("\n------------------------------ remove git ------------------------------------")
	os.system(f"rm -rf {diva_path}")
	print("Done.")


if __name__ == "__main__":

	# change nodes count?
	if len(sys.argv) <= 1:
		nodes = 7
	else:
		nodes = int(sys.argv[1])

	download()
	setup(nodes)
	start_testnet()
	input("All done? Testnet containers are stopped and repo gets deleted when continued!")
	stop_testnet()
	delete()


