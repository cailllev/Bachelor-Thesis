#!/usr/bin/python3
import os
import sys
import requests as req

from time import sleep
from pathlib import Path
from combine_texts import *

root_path = Path(__file__).parent / ".."
diva_path = Path(__file__).parent / "../diva-dockerized/"


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


def setup(nodes):

	# create and write yml file (controls nodes and dbs)
	print("\n------------------------------ adapt yml file --------------------------------")
	print("Changing yml file to create local-testnet with " + str(nodes) + " nodes.")
	yaml_content = combine(nodes)
	yaml_name = f"{diva_path}/docker-compose/local-testnet.yml"

	with open(yaml_name, "w") as f:
		f.write(yaml_content)


def start_testnet():
	
	print("\n------------------------------ start testnet ---------------------------------")
	os.system(f"sudo docker-compose -f {diva_path}/docker-compose/local-testnet.yml up -d")
	
	print("\n------------------------------ test connection -------------------------------")
	print("Testnet is up and running, sending test-request to diva-api/about and explorer...")

	api_responsive = False
	explorer_responsive = False

	while not api_responsive or not explorer_responsive:
		try:
			if not api_responsive:
				res = req.get("http://172.29.101.30:19012/about")
				print("Got 200 response from API: " + str(res.status_code == 200))
				api_responsive = True

			if not explorer_responsive:
				res = req.get("http://172.29.101.100:3920/")
				print("Got 200 response from Explorer: " + str(res.status_code == 200))
				explorer_responsive = True
		
		except req.exceptions.RequestException:
			print("No connection, wait for 3 sec...")
			sleep(3)


def cleanup():
	print("\n------------------------------ docker diva volumes down ----------------------")
	os.system(f"sudo docker-compose -f {diva_path}/docker-compose/local-testnet.yml down --volumes")

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
	cleanup()

