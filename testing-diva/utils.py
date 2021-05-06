from setup.setup import API, EXPLORER, keys_path

from dateutil.parser import parse as date_parse
from threading import Thread
from time import sleep

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
			commands = transactions[t]["payload"]["reducedPayload"]["commands"]

			for c in commands:
				val = commands[c]["setAccountDetail"]["key"]
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
		node_name = output.split(".")[0]
		signers.append(node_name)

	return signers


def stop_nodes(lower, upper):
	for i in range (lower, upper+1):
		t = Thread(target=stop_node, args=(i,))
		t.start()


def stop_node(i):
	os.system(f"sudo docker stop n{i}.testnet.diva.local n{i}.db.testnet.diva.local")
	

def start_nodes(lower, upper):
	for i in range (lower, upper+1):
		t = Thread(target=start_node, args=(i,))
		t.start()


def start_node(i):
	os.system(f"sudo docker start n{i}.testnet.diva.local n{i}.db.testnet.diva.local")


def get_peers():
	res = req.get(f"{EXPLORER}/peers")
	return json.loads(res.text)["peers"]


def remove_peer(name):
	pub_key = open(f"{keys_path}/n{name}.pub", "r").readlines()[0]

	try:
		res = req.get(f"{API}/peer/remove?key={pub_key}", timeout=30)
		print(f"[#] Removed peer {name}")
		
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
			commands = transactions[t]["payload"]["reducedPayload"]["commands"]

			for c in commands:		
				if "removePeer" in c:
					return commands[c]["removePeer"]["publicKey"] == pub_key

	except KeyError as e:
		print("[!] Malformed block! KeyError on key:", str(e))
		return False


def render_results_P1(res):
	s = "\n------------------------------ results ---------------------------------------\n"
	if len(res) == 0:
		return s + "[!] No results."

	if len(res[0]) == 4:	
		#                   v14             v13             v13
		s += " stopped nodes | ping at [sec] | signs on ping | signers \n" 
		s += "------------------------------------------------------------------------------\n" 
		for r in res:
			s += f"{str(r[0]).rjust(14)} | {str(r[1]).rjust(13)} | {str(r[2]).rjust(13)} | "

			if "--no " in r[3]:
				s += r[3]
			else:
				s += ', \t'.join(r[3])
			s += "\n"

		return s

	else:
		return "[!] Malformed results!\n" + str(results)


def render_results_P2(res):
	s = "\n------------------------------ results ---------------------------------------\n"
	if len(res) == 0:
		return s + "[!] No results."

	if len(res[0]) == 4:	
		#                   v14            v16               v15
		s += " stopped nodes | removed peer | signs on remove | signers \n" 
		s += "------------------------------------------------------------------------------\n" 
		for r in res:
			s += f"{str(r[0]).rjust(14)} | {str(r[1]).rjust(16)} | {str(r[2]).rjust(15)} | "

			if "--no " in r[3]:
				s += r[3]
			else:
				s += ', \t'.join(r[3])
			s += "\n"

		return s

	else:
		return "[!] Malformed results!\n" + str(results)


def render_results_P3(res):
	s = "\n------------------------------ results ---------------------------------------\n"
	if len(res) == 0:
		return s + "[!] No results."

	if len(res[0]) == 4:	
		#                   v14             v13             v13
		s += " running nodes | ping at [sec] | signs on ping | signers \n" 
		s += "------------------------------------------------------------------------------\n" 
		for r in res:
			s += f"{str(r[0]).rjust(14)} | {str(r[1]).rjust(13)} | {str(r[2]).rjust(13)} | "

			if "--no " in r[3]:
				s += r[3]
			else:
				s += ', \t'.join(r[3])
			s += "\n"

		return s

	else:
		return "[!] Malformed results!\n" + str(results)
