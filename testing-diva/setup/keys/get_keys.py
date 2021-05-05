#!/usr/bin/python3
# python3 setup/keys/get_keys.py

import os

from pathlib import Path
from os.path import isfile


yml_file = Path(__file__).parent / "local_testnet.yml"
keys_path = Path(__file__).parent / "."


def up():
	os.system(f"sudo docker system prune -f")
	os.system(f"sudo docker network prune -f")
	os.system(f"sudo docker volume prune -f")
	os.system(f"sudo docker-compose -f {yml_file} up -d")

	print("[*] Created and started iroha container.")

def down():
	os.system(f"sudo docker-compose -f {yml_file} down --volumes")


def get_keys():

	# test if keys already exists
	for i in range(1, 7+1):
		if isfile(f"{keys_path}/n{i}.priv"):
			ans = input("[#] Keys already exists, do you want to overwrite them? [y/N]")
			if ans not in ["y", "yes", "Y", "Yes"]:
				print("[#] Aborting! Please wait.")
				down()
				exit()
			else:
				break

	up()

	for i in range(1, 7+1):
		os.system(f"sudo docker cp n{i}.testnet.diva.local:/opt/iroha/data/n{i}.pub {keys_path}")
		os.system(f"sudo docker cp n{i}.testnet.diva.local:/opt/iroha/data/n{i}.priv {keys_path}")

	print(f"[*] Copied all keys.")

	down()

if __name__ == "__main__":
	get_keys()