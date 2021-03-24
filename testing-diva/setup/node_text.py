#!/usr/bin/python3

def node_text(node_nr, nodes_count, offset):
  string = f"\
  n{node_nr}.testnet.diva.local:\n\
    container_name: n{node_nr}.testnet.diva.local\n\
    image: divax/iroha:latest\n\
    restart: unless-stopped\n\
    environment:\n\
      IP_POSTGRES: 172.29.101.{node_nr}\n\
      NAME_PEER: n{node_nr}\n\
      BLOCKCHAIN_NETWORK: testnet.diva.local\n\
    volumes:\n\
      - n{node_nr}.testnet.diva.local:/opt/iroha/\n\
    networks:\n\
      network.testnet.diva.local:\n\
        ipv4_address: 172.29.101.{node_nr + offset}\n\
    extra_hosts:\n"
  
  for i in range(nodes_count):
    string += f"      - n{i+1}.testnet.diva.local:172.29.101.{i+1+offset}\n"

  return string+"\n"


# test if created is correct
if __name__ == "__main__":
  
  created = node_text(1, 7)
  
  correct = "\
  n1.testnet.diva.local:\n\
    container_name: n1.testnet.diva.local\n\
    image: divax/iroha:latest\n\
    restart: unless-stopped\n\
    environment:\n\
      IP_POSTGRES: 172.29.101.11\n\
      NAME_PEER: n1\n\
      BLOCKCHAIN_NETWORK: testnet.diva.local\n\
    volumes:\n\
      - n1.testnet.diva.local:/opt/iroha/\n\
    networks:\n\
      network.testnet.diva.local:\n\
        ipv4_address: 172.29.101.21\n\
    extra_hosts:\n\
      - n1.testnet.diva.local:172.29.101.21\n\
      - n2.testnet.diva.local:172.29.101.22\n\
      - n3.testnet.diva.local:172.29.101.23\n\
      - n4.testnet.diva.local:172.29.101.24\n\
      - n5.testnet.diva.local:172.29.101.25\n\
      - n6.testnet.diva.local:172.29.101.26\n\
      - n7.testnet.diva.local:172.29.101.27\n\n"

  print(created == correct)