#!/usr/bin/python3

def node_text(node_ip, node_nr, node_ips, node_nrs):
  string = f"\
  n{node_nr}.testnet.diva.local:\n\
    container_name: n{node_nr}.testnet.diva.local\n\
    image: divax/iroha:latest\n\
    restart: unless-stopped\n\
    environment:\n\
      IP_POSTGRES: 172.29.101.{node_ip-1}\n\
      NAME_PEER: n{node_nr}\n\
      BLOCKCHAIN_NETWORK: testnet.diva.local\n\
    volumes:\n\
      - n{node_nr}.testnet.diva.local:/opt/iroha/\n\
    networks:\n\
      network.testnet.diva.local:\n\
        ipv4_address: 172.29.101.{node_ip}\n\
    extra_hosts:\n"
  
  for ip,nr in zip(node_ips, node_nrs):
    string += f"      - n{nr}.testnet.diva.local:172.29.101.{ip}\n"

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