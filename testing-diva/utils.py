from setup.setup import EXPLORER

from dateutil.parser import parse as date_parse
from threading import Thread

import os
import json
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
	

def stop_nodes(lower, upper):
	for i in range (lower, upper+1):
		t = Thread(target=stop_node, args=(i,))
		t.start()


def stop_node(i):
	os.system(f"sudo docker stop n{i}.testnet.diva.local n{i}.db.testnet.diva.local")


def render_results(res):
	s = "\n------------------------------ results ---------------------------------------\n"
	if len(res) == 0:
		return s + "[!] No results."

	# test if one or 2 pings 
	# res = [(i, signs_1, signs_2), (...), ...] or
	# res = [(i, signs_1), (...), ...]
	if len(res[0]) == 3:	
		#                   v14              v14              v14
		s += " running nodes | 1st ping signs | 2nd ping signs \n" 
		s += "------------------------------------------------ \n" 
		for r in res:
			s += f"{str(r[0]).rjust(14)} | {str(r[1]).rjust(14)} | {str(r[2]).rjust(14)} \n"

		return s

	elif len(res[0]) == 2:	
		#                   v14              v14
		s += " running nodes | signs on ping  \n" 
		s += "------------------------------- \n" 
		for r in res:
			s += f"{str(r[0]).rjust(14)} | {str(r[1]).rjust(14)} \n"

		return s

	return "[!] Malformed results!\n" + str(results)
