#!/usr/bin/python3
import os
import sys

from pathlib import Path
from combine_texts import *

path = Path(__file__).parent / "diva-dockerized"

# rm old git
os.system(f"rm -r diva-dockerized")

# clone git
os.system("git clone -b develop https://codeberg.org/diva.exchange/diva-dockerized.git")

# change nodes count?
if not sys.argv[1]:
	nodes = 7
else:
	nodes = sys.argv[1]

yaml_content = combine(nodes)
yaml_name = path + "local-testnet.yml"


with open(yaml_name, "w") as f:
	f.write(yaml_content)
