#!/usr/bin/python3

# normal usage from parent dir
try:
  from setup.node_db_text import *
  from setup.node_text import *

# direct usage from current dir
except ModuleNotFoundError:
  from node_db_text import *
  from node_text import *


# nodes_dbs_ip = "172.29.101.10 + node_nr" 
# max ip = 255
# reserved ips = 0, 1, 30 (API Endpoint), 100 (Explorer), 255
# Torii -> n1 ip ??

dbs_ips = list(range(11,29,2))
dbs_ips.extend(list(range(31,99,2)))
dbs_ips.extend(list(range(103,255,2)))

nodes_ips = list(range(12,30,2))
nodes_ips.extend(list(range(32,100,2)))
nodes_ips.extend(list(range(104,256,2)))

max_nodes = offset = 100
n1_ip = "172.29.101." + str(nodes_ips[0])


def combine(nodes_count):

	assert nodes_count < max_nodes, f"[!] Max 100 nodes allowed, {nodes_count} are too much!"

	header = "\
#\n\
# Copyright (C) 2020 diva.exchange\n\
#\n\
# This program is free software: you can redistribute it and/or modify\n\
# it under the terms of the GNU Affero General Public License as published by\n\
# the Free Software Foundation, either version 3 of the License, or\n\
# (at your option) any later version.\n\
#\n\
# This program is distributed in the hope that it will be useful,\n\
# but WITHOUT ANY WARRANTY; without even the implied warranty of\n\
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n\
# GNU Affero General Public License for more details.\n\
#\n\
# You should have received a copy of the GNU Affero General Public License\n\
# along with this program.  If not, see <https://www.gnu.org/licenses/>.\n\
#\n\
# Author/Maintainer: Konrad Bächler <konrad@diva.exchange>\n\
#\n\n\
version: \"3.7\"\n\
services:\n"
	
	numbers = list(range(1, len(nodes_ips) + 1))
	numbers = numbers[:nodes_count]
	nodes = [node_text(ip, nr, nodes_ips, numbers) for ip, nr in zip(nodes_ips, numbers)]
	nodes_dbs = [node_db_text(ip, nr) for ip, nr in zip(dbs_ips, numbers)]

	nodes_all = ""
	for i in range(nodes_count):
		nodes_all += nodes_dbs[i] + nodes[i]

	api = "\
  api.testnet.diva.local:\n\
    container_name: api.testnet.diva.local\n\
    image: divax/diva-api:latest\n\
    restart: unless-stopped\n\
    environment:\n\
      NODE_ENV: development\n\
      IP_LISTEN: 0.0.0.0\n\
      PORT_LISTEN: 19012\n\
      API_ENDPOINT: 172.29.101.30:19012\n\
      TORII: ${TORII:-"+n1_ip+":50051}\n\
      CREATOR: diva@testnet.diva.local\n\
      I2P_HOSTNAME: ${I2P_HOSTNAME:-127.0.0.1}\n\
      I2P_HTTP_PROXY_PORT: ${I2P_HTTP_PROXY_PORT:-4444}\n\
      I2P_WEBCONSOLE_PORT: ${I2P_WEBCONSOLE_PORT:-7070}\n\
      PATH_IROHA: /tmp/iroha/\n\
    volumes:\n\
      - api.testnet.diva.local:/home/node/data/\n\
      - n1.testnet.diva.local:/tmp/iroha/\n\
    networks:\n\
      network.testnet.diva.local:\n\
        ipv4_address: 172.29.101.30\n\n"

	explorer = "\
  explorer.testnet.diva.local:\n\
    container_name: explorer.testnet.diva.local\n\
    image: divax/iroha-explorer:latest\n\
    restart: unless-stopped\n\
    environment:\n\
      IP_EXPLORER: 0.0.0.0\n\
      PORT_EXPLORER: 3920\n\
      PATH_IROHA: /tmp/iroha/\n\
    volumes:\n\
      - n1.testnet.diva.local:/tmp/iroha/:ro\n\
      - explorer.testnet.diva.local:/home/node/\n\
    networks:\n\
      network.testnet.diva.local:\n\
        ipv4_address: 172.29.101.100\n\n"

	networks = "\
networks:\n\
  network.testnet.diva.local:\n\
    internal: true\n\
    name: network.testnet.diva.local\n\
    ipam:\n\
      driver: default\n\
      config:\n\
        - subnet: 172.29.101.0/24\n\n"

	volumes = "\
volumes:\n"

	for i in range(nodes_count):
		volumes += f"\
  n{i+1}.testnet.diva.local:\n\
    name: n{i+1}.testnet.diva.local\n"

	for i in range(nodes_count):
		volumes += f"\
  n{i+1}.db.testnet.diva.local:\n\
    name: n{i+1}.db.testnet.diva.local\n"

	volumes += "\
  api.testnet.diva.local:\n\
    name: api.testnet.diva.local\n\
  explorer.testnet.diva.local:\n\
    name: explorer.testnet.diva.local\n"

	return header+nodes_all+api+explorer+networks+volumes


# test if created is correct
if __name__ == "__main__":

  from pathlib import Path
  import re
  ip = re.compile(r"([0-9]+\.){3}[0-9]+")

  compare_file = Path(__file__).parent / "local-testnet_compare.yml.txt"
  correct = "".join(open(compare_file).readlines())

  created = combine(7)
  diff_count = 0
  diff_ip = 0

  for l1, l2 in zip(correct.split("\n"), created.split("\n")):
    if l1 != l2:
      if not ip.search(l1) and not ip.search(l2): # ignore different ips
        print("correct:  " + l1)
        print("created:  " + l2 + "\n")
        diff_count += 1
      else:
        diff_ip += 1


  print("Files are the same? ", correct == created)
  print("Diff IPs:   ", diff_ip)
  print("Diff other: ", diff_count)
