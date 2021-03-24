#!/usr/bin/python3

def node_db_text(node_nr):
  return f"\
  n{node_nr}.db.testnet.diva.local:\n\
    container_name: n{node_nr}.db.testnet.diva.local\n\
    image: postgres:10-alpine\n\
    command: -c max_prepared_transactions=100\n\
    restart: unless-stopped\n\
    environment:\n\
      POSTGRES_DATABASE: iroha\n\
      POSTGRES_USER: iroha\n\
      POSTGRES_PASSWORD: iroha\n\
    volumes:\n\
      - n{node_nr}.db.testnet.diva.local:/var/lib/postgresql/data/\n\
    networks:\n\
      network.testnet.diva.local:\n\
        ipv4_address: 172.29.101.{node_nr}\n\n"


# test if created is correct
if __name__ == "__main__":

  created = node_db_text(1)

  correct = f"\
  n1.db.testnet.diva.local:\n\
    container_name: n1.db.testnet.diva.local\n\
    image: postgres:10-alpine\n\
    command: -c max_prepared_transactions=100\n\
    restart: unless-stopped\n\
    environment:\n\
      POSTGRES_DATABASE: iroha\n\
      POSTGRES_USER: iroha\n\
      POSTGRES_PASSWORD: iroha\n\
    volumes:\n\
      - n1.db.testnet.diva.local:/var/lib/postgresql/data/\n\
    networks:\n\
      network.testnet.diva.local:\n\
        ipv4_address: 172.29.101.11\n\n"

  print(correct == created)