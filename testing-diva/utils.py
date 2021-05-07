from setup.setup import API, EXPLORER, keys_path

from dateutil.parser import parse as date_parse
from threading import Thread
from pprint import pprint
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
	os.system(f"sudo docker stop n{i}.testnet.diva.local n{i}.db.testnet.diva.local")
	

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
	print(f"[#] Trying to remove peer n{name} with timeout of {t} sec.")
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


def render_results_P1(res):
	s = "\n------------------------------ results ---------------------------------------\n"
	if len(res) == 0:
		return s + "[!] No results."

	if len(res[0]) == 4:	
		#                   v14             v13             v13
		s += " stopped peers | ping at [sec] | signs on ping | signers \n" 
		s += "------------------------------------------------------------------------------\n" 
		for r in res:
			s += f"{str(r[0]).rjust(14)} | {str(r[1]).rjust(13)} | {str(r[2]).rjust(13)} | "

			if "--no " in r[3]:
				s += r[3]
			else:
				for signer in r[3]:
					s += str(signer).rjust(3) + ", "
				s = s[:-2]
			s += "\n"

		return s

	else:
		return "[!] Malformed results!\n" + str(results)


def render_results_P2(res):
	s = "\n------------------------------ results ---------------------------------------\n"
	if len(res) == 0:
		return s + "[!] No results."

	if len(res[0]) == 4:	
		#                   v14            v12               v15
		s += " started peers | removed peer | signs on remove | signers \n" 
		s += "------------------------------------------------------------------------------\n" 
		for r in res:
			s += f"{str(r[0]).rjust(14)} | {str(r[1]).rjust(12)} | {str(r[2]).rjust(15)} | "

			if "--no " in r[3]:
				s += r[3]
			else:
				for signer in r[3]:
					s += str(signer).rjust(3) + ", "
				s = s[:-2]
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
		s += " running peers | ping at [sec] | signs on ping | signers \n" 
		s += "------------------------------------------------------------------------------\n" 
		for r in res:
			s += f"{str(r[0]).rjust(14)} | {str(r[1]).rjust(13)} | {str(r[2]).rjust(13)} | "

			if "--no " in r[3]:
				s += r[3]
			else:
				for signer in r[3]:
					s += str(signer).rjust(3) + ", "
				s = s[:-2]
			s += "\n"

		return s

	else:
		return "[!] Malformed results!\n" + str(results)
