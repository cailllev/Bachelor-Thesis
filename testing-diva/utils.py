from setup.setup import API, EXPLORER, keys_path

from dateutil.parser import parse as date_parse
from threading import Thread

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
		val = block["blockV1"]["payload"]["transactions"][0]["payload"]["reducedPayload"]["commands"][0]["setAccountDetail"]["key"]
		return val == "ping"
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


# HTTPConnectionPool(host='172.29.101.30', port=19012): Max retries exceeded with url: /peer/remove?key=67549f3f31403d99f57b0d741b3bce16fc6e5a3d76d74a14c6adf25ccca36089 (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f1a9ef7eaf0>: Failed to establish a new connection: [Errno 111] Connection refused'))
def remove_peer(name):
	print(req.get(f"{API}/blockstore").text)
	pub_key = open(f"{keys_path}/n{name}.pub", "r").readlines()[0]
	url = f"{API}/peer/remove?key={pub_key}"
	print(url)
	res = req.get(url)
	print(f"[#] Remove peer {name}: {res.text}")


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
				s += ', '.join(r[3])
			s += "\n"

		return s

	else:
		return "[!] Malformed results!\n" + str(results)


def render_results_P2(res):
	s = "\n------------------------------ results ---------------------------------------\n"
	if len(res) == 0:
		return s + "[!] No results."

	if len(res[0]) == 4:	
		#                   v14                v16             v13
		s += " stopped nodes | removed at [sec] | signs on ping | signers \n" 
		s += "------------------------------------------------------------------------------\n" 
		for r in res:
			s += f"{str(r[0]).rjust(14)} | {str(r[1]).rjust(16)} | {str(r[2]).rjust(13)} | "

			if "--no " in r[3]:
				s += r[3]
			else:
				s += ', '.join(r[3])
			s += "\n"

		return s

	else:
		return "[!] Malformed results!\n" + str(results)


def render_results_P3(res):
	s = "\n------------------------------ results ---------------------------------------\n"
	if len(res) == 0:
		return s + "[!] No results."

	if len(res[0]) == 2:	
		#                   v14              v14
		s += " running nodes | signs on ping  \n" 
		s += "------------------------------------------------------------------------------\n" 
		for r in res:
			s += f"{str(r[0]).rjust(14)} | {str(r[1]).rjust(14)} \n"

		return s

	else:
		return "[!] Malformed results!\n" + str(results)
