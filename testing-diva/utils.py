# is not runnable on it's own (makes no sense)


from setup.setup import API, EXPLORER, keys_path
from setup.combine_texts import peers_ips

from dateutil.parser import parse as date_parse
from threading import Thread
from time import sleep, time
from math import floor
from pprint import pprint

import os
import json
import subprocess
import requests as req


def get_blocks():
	res = req.get(f"{EXPLORER}/blocks")
	return json.loads(res.text)["blocks"]


def get_block_number(block):
	return int(block['blockV1']['payload']['height'])


def get_signatures(block):
	return block['blockV1']['signatures']


def get_id(block):
	return block['id']


def get_creation_date(block):
	return date_parse(block['dateTimeFormatted'])


def get_transactions_count(block):
	return block['lengthTransactions']


def is_ping(block):
	try:
		transactions = block["blockV1"]["payload"]["transactions"]

		for t in transactions:
			commands = t["payload"]["reducedPayload"]["commands"]

			for c in commands:
				val = c["setAccountDetail"]["key"]
				if val == "ping":
					return True

	except KeyError as e:
		print("[!] Malformed block! KeyError on key:", str(e))
		return False


def get_signers(block):
	signatures = block["blockV1"]["signatures"]
	signers = []

	for sign in signatures:
		output = subprocess.check_output(f'grep -F {sign["publicKey"]} {keys_path}/*.pub', shell=True).decode()
		output = output.split("/")[-1]
		peer_name = output.split(".")[0]
		signers.append(peer_name)

	return signers


def stop_peers(lower, upper):
	T = []
	for i in range (lower, upper+1):
		t = Thread(target=stop_peer, args=(i,))
		t.start()
		T.append(t)

	for t in T:
		t.join()


def stop_peer(i):
	os.system(f"sudo docker stop n{i}.db.testnet.diva.local n{i}.testnet.diva.local")
	

def start_peers(lower, upper):
	T = []
	for i in range (lower, upper+1):
		t = Thread(target=start_peer, args=(i,))
		t.start()
		T.append(t)

	for t in T:
		t.join()


def start_peer(i):
	os.system(f"sudo docker start n{i}.testnet.diva.local n{i}.db.testnet.diva.local")


def get_peers():
	res = req.get(f"{EXPLORER}/peers")
	return json.loads(res.text)["peers"]


def remove_peer(name, t):
	pub_key = open(f"{keys_path}/n{name}.pub", "r").readlines()[0]

	try:
		res = req.get(f"{API}/peer/remove?key={pub_key}", timeout=t)
		
	except req.exceptions.Timeout as e:
		print(f"[#] Timeout while trying to remove peer!")
				
		class res: pass
		res.status_code = 408
		
	except req.exceptions.RequestException as e:
		print(f"[#] Unexpected exception while trying to remove peer!")
		print(str(e))
				
		class res: pass
		res.status_code = 500

	return res


def is_remove_peer(block, pub_key):	
	try:
		transactions = block["blockV1"]["payload"]["transactions"]

		for t in transactions:
			commands = t["payload"]["reducedPayload"]["commands"]

			for c in commands:		
				if "removePeer" in c:
					return c["removePeer"]["publicKey"] == pub_key

	except KeyError as e:
		print("[!] Malformed block! KeyError on key:", str(e))
		return False


def sleep_till_whole_sec():
	now_s = time()
	only_ms = now_s - floor(now_s)
	sleep(1 - only_ms + 0.001) # safety margin of 1 ms


def render_results(res, peers, header, test_nr):
	s = f"\n------------------------------ results - {peers} peers total ----------------------\n"
	if len(res) == 0:
		s += "[!] No results."

	elif len(res[0]) == 4:
		s += " " + " | ".join([h for h in header]) + " \n" 
		s += "------------------------------------------------------------------------------\n" 
		for r in res:
			s += f" {str(r[0]).rjust(len(header[0]))} | {str(r[1]).rjust(len(header[1]))} | {str(r[2]).rjust(len(header[2]))} | "

			if "--" in r[3]:
				s += r[3]
			else:
				for signer in r[3]:
					s += str(signer).rjust(3) + ", "
				s = s[:-2]
			s += "\n"

	elif len(res[0]) == 5:
		s += " " + " | ".join([h for h in header]) + " \n" 
		s += "------------------------------------------------------------------------------\n" 
		for r in res:
			s += f" {str(r[0]).rjust(len(header[0]))} | {str(r[1]).rjust(len(header[1]))} | {str(r[2]).rjust(len(header[2]))} | {str(r[3]).rjust(len(header[3]))} | "

			if "--" in r[4]:
				s += r[4]
			else:
				for signer in r[4]:
					s += str(signer).rjust(4) + ", "
				s = s[:-2]
			s += "\n"

	else:
		s = "[!] Malformed results!\n" + str(res)

	file = f"results/{test_nr}_{peers}.txt"
	if os.path.exists(file):
		ans = input(f"[#] File {file} already exists! Overwrite? [y/N]")
		if ans not in ["Yes", "yes", "Y", "y"]:
			return s

	with open(file, "w") as f:
		f.write(s)

	return s
