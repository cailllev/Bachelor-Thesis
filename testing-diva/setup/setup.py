#!/usr/bin/python3
import os
import sys
import requests as req

from time import sleep
from pathlib import Path
from combine_texts import *

root_path = Path(__file__).parent / ".."
diva_path = Path(__file__).parent / "../diva-dockerized/"

# stop all old diva docker containers
os.system(f"sudo docker-compose -f {diva_path}/docker-compose/local-testnet.yml down --volumes")

# remove old git
os.system(f"rm -rf {diva_path}")

# clone diva dockerized repo
os.system(f"cd {root_path} && git clone -b develop https://codeberg.org/diva.exchange/diva-dockerized.git")

# change nodes count?
if len(sys.argv) <= 1:
	nodes = 7
else:
	nodes = int(sys.argv[1])

# create and write yml file (controls nodes and dbs)
yaml_content = combine(nodes)
yaml_name = f"{diva_path}/docker-compose/local-testnet.yml"

with open(yaml_name, "w") as f:
	f.write(yaml_content)

# start testnet
os.system(f"sudo docker-compose -f {diva_path}/docker-compose/local-testnet.yml pull && sudo docker-compose -f {diva_path}/docker-compose/local-testnet.yml up -d")

# wait (TODO: automate this)
print("--------------------------------------------------------------------------------")
print("Testnet is up and running, sending test-request to diva-api/about...")
while True:
	try:
		res = req.get("http://172.29.101.30:19012/about")
		print("Got 200 response: " + str(res.status_code == 200))
		break
	
	except req.exceptions.RequestException:
		print("No connection, wait for 3 sec...")
		sleep(3)

input("All done? Testnet containers are stopped and repo gets deleted when continued!")
print("--------------------------------------------------------------------------------")

# stop testnet
os.system(f"sudo docker-compose -f {diva_path}/docker-compose/local-testnet.yml down --volumes")

# remove git repo
os.system(f"rm -rf {diva_path}")
