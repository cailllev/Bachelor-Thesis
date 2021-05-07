#!/usr/bin/python3
# python3 setup/setup.py


import os
import sys
import json
import subprocess
import requests as req

from sys import stdout
from time import sleep
from pathlib import Path
from pprint import pprint

# normal usage from parent dir
try:
	from setup.combine_texts import *

# direct usage from current dir
except ModuleNotFoundError:
	from combine_texts import *

root_path = Path(__file__).parent / ".."
yml_file = Path(__file__).parent / "local-testnet.yml"
keys_path = Path(__file__).parent / "../setup/keys/"

TIMEOUT = 60  # sec
API = "http://172.29.101.30:19012"
EXPLORER = "http://172.29.101.100:3920"

remove_orphans = False


def download():
	print("\n------------------------------ docker stop and remove volumes ----------------")

	# check if there are containers running
	output = subprocess.check_output(["sudo", "docker", "ps", "-a"])
	running = len(output.split(b"\n")) - 2 # -1 for header and last \n
	if running > 0:
	
		# check if the original yml file is there to remove the containers
		if os.path.isfile(yml_file):
			os.system(f"sudo docker-compose -f {yml_file} down --volumes")

		else:
			print("[!] No yml file detected to stop the docker volumes.")
			remove_orphans = True

	else:
		print("[*] No containers to stop.")
	
	print("\n------------------------------ pull docker images ----------------------------")
	os.system(f"sudo docker-compose -f {root_path}/setup/docker_images_pull.yml pull")


def setup(peers, benchmark=False):

	# create and write yml file (controls peers and dbs)
	print("\n------------------------------ adapt yml file --------------------------------")
	print("[*] Changing yml file to create local-testnet with " + str(peers) + " peers.")
	yml_content = combine(peers, benchmark)
	
	if yml_content == None:  # i.e. peers over threshold and not continued and not in benchmark
		cleanup()

	with open(yml_file, "w") as f:
		f.write(yml_content)	
	

	print("\n------------------------------ create docker containers ----------------------")
	os.system("sudo docker system prune -f")
	os.system("sudo docker network prune -f")
	os.system("sudo docker volume prune -f")

	if remove_orphans:  # is only needed if different count of peers and old yml file was deleted
		print("[!] Did not down containers properly! Start containers with \"--remove-orphans\"!")
		os.system(f"sudo docker-compose -f {yml_file} up --remove-orphans --no-start")

	else:
		os.system(f"sudo docker-compose -f {yml_file} up --no-start")
	
	
	# all peers up, return without explorer and api started
	if benchmark:
		return


	print("\n------------------------------ adapt iroha genesis block ---------------------")

	res = req.get("https://codeberg.org/diva.exchange/iroha/raw/branch/main/data/local-genesis/0000000000000001")
	data = json.loads(res.text)

	pub_keys = []
	for i in range(1, peers+1):
		pub_keys.append(open(f"{keys_path}/n{i}.pub").readlines()[0])
	
	add_peer = '[' + ', '.join([f'{{"addPeer": {{"peer": {{"address": "n{i}.testnet.diva.local:10001", \
		"peerKey": "{key}"}}}}}}' for i, key in zip(range(1, peers+1), pub_keys)]) + ']'
	add_peer = json.loads(add_peer)

	commands = data["blockV1"]["payload"]["transactions"][0]["payload"]["reducedPayload"]["commands"]

	# remove all old addPeer commands
	commands = list(filter(lambda cmd: "addPeer" not in cmd, commands))

	# add new addPeers to commands
	commands = add_peer + commands 

	data["blockV1"]["payload"]["transactions"][0]["payload"]["reducedPayload"]["commands"] = commands

	with open("0000000000000001", "w") as f:
		json.dump(data, f, indent=4)

	print("[*] New genesis block created.")

	# copy new package.json to the api container
	for i in range(1, peers+1):
		print(f"\r[#] Copy genesis block into n{i}", end="")
		os.system(f"sudo docker cp 0000000000000001 n{i}.testnet.diva.local:/opt/iroha/data/local-genesis/0000000000000001")
	

	print("\r[*] Copied new genesis block to all iroha containers.")
	os.system(f"sudo rm 0000000000000001")
	

	print("\n------------------------------ copy iroha key pairs ---------------------------")
		
	for n in range(1, peers+1): # what keypair to copy
		for i in range(1, peers+1): # copy keypair n into the containers n1...n{peers+1}
			print(f"\r[#] Copy n{n}'s keypair into n{i} ...", end="")
			os.system(f"sudo docker cp {keys_path}/n{n}.priv n{i}.testnet.diva.local:opt/iroha/data/n{n}.priv")
			os.system(f"sudo docker cp {keys_path}/n{n}.pub  n{i}.testnet.diva.local:opt/iroha/data/n{n}.pub")
		
		print("\r", end="")

	print("\r[*] Added keys to iroha containers.")


def start_testnet(peers, benchmark=False):

	print("\n------------------------------ start the containers --------------------------")
	os.system(f"sudo docker-compose -f {yml_file} up -d")

	print("\n------------------------------ test connection -------------------------------")
	print("[*] Testnet is up and running, sending test-request to diva-api/about and explorer.")

	api_responsive = False
	explorer_responsive = False
	time = 0
	TIMEOUT = 120 # should not take longer than 1 min to start and get first response from explorer

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
			print(f"[#] No connection, waited for {time} sec...")
			time += 5
			sleep(5)

		if not ok_response:
			print(f"[#] Connected, but res not 200 yet. API: {api_res_code}, Explorer: {exporer_res_code}, wait for 3 sec...")
			time += 5
			sleep(5)

	def get_peers():
		res = req.get(f"{EXPLORER}/peers")
		return json.loads(res.text)["peers"]

	# now wait for (or check if) all peers in the newwork
	waiting = 0
	TIMEOUT = 240  # after 3 min they should be up (if done manually, instant if done with genesis block)

	up = len(get_peers())
	while up < peers:
		print(f"[#] Only {up} peers registered out of {peers}, waited for {waiting} sec...")
		sleep(15)
		waiting += 15

		up = len(get_peers())

		if waiting >= TIMEOUT:
			return False

	print(f"[*] All {peers} peers registered as peers, {up} total peers.")

	# returns True if not TIMEOUT but all peers up
	return True	


def stop_testnet():
	print("\n------------------------------ docker volumes down ---------------------------")
	os.system(f"sudo docker-compose -f {yml_file} down")


def delete():
	print("\n------------------------------ docker remove all -----------------------------")
	os.system(f"sudo docker system prune -f")
	os.system(f"sudo docker network prune -f")
	os.system(f"sudo docker volume prune -f")


if __name__ == "__main__":

	# change peers count?
	if len(sys.argv) < 2:
		peers = 9
	else:
		peers = int(sys.argv[1])

	try: 
		download()
		setup(peers)
		start_testnet(peers)
		input("[*] All done? Testnet containers are stopped and deleted when continued!")
	
	except KeyboardInterrupt:
		print("[!] Aborting setup! Please wait!")
	
	except BaseException as e:
		print("[!] Unexpected Error! Aborting setup, please wait!")
		print("[!] ->" + str(e))

	finally:
		stop_testnet()
		delete()
