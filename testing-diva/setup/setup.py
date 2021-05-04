#!/usr/bin/python3
import os
import sys
import json
import subprocess
import requests as req

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
diva_path = Path(__file__).parent / "../diva-dockerized/"
yml_file = Path(__file__).parent / "local-testnet.yml"

TIMEOUT = 60  # sec
API = "http://172.29.101.30:19012"
EXPLORER = "http://172.29.101.100:3920"

remove_orphans = False


def download():
	print("\n------------------------------ docker diva volumes down ----------------------")

	# check if there are containers running
	output = subprocess.check_output(["sudo", "docker", "ps", "-a"])
	running = len(output.split(b"\n")) - 2 # -1 for header and last \n
	if running > 0:
	
		# check if the original yml file is there to delete the containers
		if os.path.isfile(yml_file):
			os.system(f"sudo docker-compose -f {yml_file} down --volumes")

		else:
			print("[!] No yml file detected to down the docker volumes.")
			remove_orphans = True
			pprint(output)
			print(running)

	else:
		print("[*] No containers to down.")

	print("\n------------------------------ remove old git --------------------------------")
	os.system(f"rm -rf {diva_path}")
	print("[*] Done.")

	print("\n------------------------------ clone repo ------------------------------------")
	os.system(f"cd {root_path} && git clone -b develop https://codeberg.org/diva.exchange/diva-dockerized.git")
	
	print("\n------------------------------ pull docker images ----------------------------")
	os.system(f"sudo docker-compose -f {root_path}/setup/docker_images_pull.yml pull")


def setup(nodes, benchmark=False):

	# create and write yml file (controls nodes and dbs)
	print("\n------------------------------ adapt yml file --------------------------------")
	print("[*] Changing yml file to create local-testnet with " + str(nodes) + " nodes.")
	yml_content = combine(nodes, benchmark)
	
	if yml_content == None:  # i.e. nodes over threshold and not continued and not in benchmark
		cleanup()

	with open(yml_file, "w") as f:
		f.write(yml_content)


def start_testnet(nodes, benchmark=False):
	
	print("\n------------------------------ start testnet ---------------------------------")
	os.system("sudo docker system prune -f")

	if remove_orphans:  # is only needed if different count of NODES and old yml file was deleted
		print("[!] Did not down containers properly! Start containers with \"--remove-orphans\"!")
		os.system(f"sudo docker-compose -f {yml_file} up --remove-orphans --no-start")

	else:
		os.system(f"sudo docker-compose -f {yml_file} up --no-start")
	
	
	# all nodes up, return true without explorer and api started
	if benchmark:
		return True

	"""
	print("\n------------------------------ adapt api container ---------------------------")

	# create new package.json to include all the nodes
	res = req.get("https://codeberg.org/diva.exchange/diva-api/raw/branch/main/package.json")
	data = json.loads(res.text)

	node_names = '"' + '", "'.join([f'n{i}.testnet.diva.local' for i in range(1, nodes+1)]) + '"'
	peer_endpoints = '[["' + '"], ["'.join([f'172.29.101.{ip}:10001", "n{i}.testnet.diva.local' for ip,i in zip(nodes_ips, range(1, nodes+1))]) + '"]]'

	dev_diva_api_content = f' \
	{{"bootstrap_peer": \
		[{node_names}], \
		"i2p_hostname": "172.20.101.200", \
		"i2p_port_http_proxy": 4444, \
		"i2p_port_webconsole": 7070, \
		"ip_listen": "0.0.0.0", \
		"log_level": "trace", \
		"log_name": "devDivaApi", \
		"path_iroha": "/tmp/iroha", \
		"port_listen": 19012, \
		"torii": "{n1_ip}:50051", \
    	"creator": "diva@testnet.diva.local", \
    	"api_endpoint": "localhost:19012", \
    	"array_peer_endpoint": {peer_endpoints} \
	}}'
	
	diva_api_content = f' \
	{{"bootstrap_peer": \
		[{node_names}], \
		"i2p_hostname": "172.20.101.200", \
		"i2p_port_http_proxy": 4444, \
		"i2p_port_webconsole": 7070, \
		"ip_listen": "0.0.0.0", \
		"log_level": "info", \
		"log_name": "DivaApi", \
		"path_iroha": "/tmp/iroha", \
		"port_listen": 19012, \
		"torii": "172.20.101.3:50051" \
	}}'

	dev_diva_api_content = json.loads(dev_diva_api_content)
	data["devDivaApi"] = dev_diva_api_content
	
	diva_api_content = json.loads(diva_api_content)
	data["DivaApi"] = diva_api_content

	with open("package.json", "w") as f:
		json.dump(data, f, indent=4)

	print("[*] New package.json created.")

	# copy new package.json to the api container
	os.system("sudo docker cp package.json api.testnet.diva.local:/home/node/package.json")
	os.system("rm package.json")
	print("[*] Copied new package.json to new api container.")

	"""
	print("\n------------------------------ adapt iroha genesis block ---------------------")

	res = req.get("https://codeberg.org/diva.exchange/iroha/raw/branch/main/data/local-genesis/0000000000000001")
	data = json.loads(res.text)
	
	add_peer = '[' + ', '.join([f'{{"addPeer": {{"peer": {{"address": "n{i}.testnet.diva.local:10001", "peerKey": "6611c5accd8643f30bda43088171e471471b1494c791eaf14f070c174ee75162"}}}}}}' for i in range(8, nodes+1)]) + ']'
	add_peer = json.loads(add_peer)

	commands = data["blockV1"]["payload"]["transactions"][0]["payload"]["reducedPayload"]["commands"]
	commands = commands[:7] + add_peer + commands[7:]

	data["blockV1"]["payload"]["transactions"][0]["payload"]["reducedPayload"]["commands"] = commands

	with open("0000000000000001", "w") as f:
		json.dump(data, f, indent=4)

	print("[*] New genesis block created.")

	# copy new package.json to the api container
	for i in range(1, nodes+1):
		os.system(f"sudo docker cp 0000000000000001 n{i}.testnet.diva.local:/opt/iroha/data/local-genesis/0000000000000001")
	
	print("[*] Copied new genesis block to all iroha containers.")
	os.system(f"sudo rm 0000000000000001")

	
	print("\n------------------------------ start containers ------------------------------")
	os.system(f"sudo docker-compose -f {yml_file} up -d")

	print("\n------------------------------ test connection -------------------------------")
	print("[*] Testnet is up and running, sending test-request to diva-api/about and explorer.")

	api_responsive = False
	explorer_responsive = False
	time = 0
	TIMEOUT = 60 # should not take longer than 1 min to start and get first response from explorer

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

	# now wait for all peers to be added to the newwork
	waiting = 0
	TIMEOUT = 2400  # after 3 min they should be up

	up = len(get_peers())
	while up < nodes:
		print(f"[#] Only {up} peers registered out of {nodes}, waited for {waiting} sec...")
		sleep(15)
		waiting += 15

		up = len(get_peers())

		if waiting >= TIMEOUT:
			return False

	print(f"[*] All {nodes} nodes registered as peers.")

	# returns True if not TIMEOUT but all peers up
	return True	


def stop_testnet():
	print("\n------------------------------ docker diva volumes down ----------------------")
	os.system(f"sudo docker-compose -f {yml_file} down --volumes")
	os.system(f"sudo docker network prune -f")


def delete():
	print("\n------------------------------ remove git ------------------------------------")
	os.system(f"rm -rf {diva_path}")
	print("[*] Done.")


if __name__ == "__main__":

	# change nodes count?
	if len(sys.argv) <= 1:
		nodes = 10
	else:
		nodes = int(sys.argv[1])

	try: 
		download()
		setup(nodes)
		start_testnet(nodes)
		input("[*] All done? Testnet containers are stopped and local diva-repo gets deleted when continued!")
	
	except KeyboardInterrupt:
		print("[!] Aborting setup! Please wait!")
	
	except BaseException as e:
		print("[!] Unexpected Error! Aborting setup, please wait!")
		print("[!] ->" + str(e))

	finally:
		stop_testnet()
		delete()
