#!/usr/bin/python3
# python3 setup/keys/get_keys.py 30

import os
import sys

from pathlib import Path
from os.path import isfile

if len(sys.argv) < 2:
	print("[#] Usage: python3 gen_keys.py [amount of keys]")
	exit()

setup_iroha = Path(__file__).parent / "setup_iroha.yml"
keys_path = Path(__file__).parent / "."

keys_to_gen = int(sys.argv[1])


def up():
	os.system(f"sudo docker system prune -f")
	os.system(f"sudo docker network prune -f")
	os.system(f"sudo docker volume prune -f")
	os.system(f"sudo docker-compose -f {setup_iroha} up -d")

	print("[*] Created and started iroha container.")

def down():
	os.system(f"sudo docker-compose -f {setup_iroha} down --volumes")


def gen_keys():

	# test if keys already exists
	for i in range(8, keys_to_gen+1):
		if isfile(f"{keys_path}/n{i}.priv"):
			ans = input("[#] Keys already exists, do you want to overwrite them? [y/N]")
			if ans not in ["y", "yes", "Y", "Yes"]:
				print("[#] Aborting! Please wait.")
				down()
				exit()
			else:
				break

	up()

	cmd = "bash -c '"
	for i in range(8, keys_to_gen+1): # n1...n7 already have keys
		cmd += f"iroha-cli --new_account --account_name n{i} && "

	cmd = cmd[:-4] + "'"
	print(f"[*] Created command to create keys -> \"{cmd[:63]}...\"")
	os.system(f"sudo docker exec -d n1.testnet.diva.local {cmd}")
	print(f"[*] Created keys from n{8} ... n{keys_to_gen}.")

	for i in range(8, keys_to_gen+1): # n1...n7 already have keys
		os.system(f"sudo docker cp n1.testnet.diva.local:/opt/iroha/n{i}.pub {keys_path}")
		os.system(f"sudo docker cp n1.testnet.diva.local:/opt/iroha/n{i}.priv {keys_path}")

	print(f"[*] Copied all keys.")

	down()

if __name__ == "__main__":
	gen_keys()