# python3 peer_db_text.py
# -> can be run from any folder

def peer_db_text(peer_ip, peer_nr):
  return f"\
  n{peer_nr}.db.testnet.diva.local:\n\
    container_name: n{peer_nr}.db.testnet.diva.local\n\
    image: postgres:10-alpine\n\
    command: -c max_prepared_transactions=100\n\
    restart: unless-stopped\n\
    environment:\n\
      POSTGRES_DATABASE: iroha\n\
      POSTGRES_USER: iroha\n\
      POSTGRES_PASSWORD: iroha\n\
    volumes:\n\
      - n{peer_nr}.db.testnet.diva.local:/var/lib/postgresql/data/\n\
    networks:\n\
      network.testnet.diva.local:\n\
        ipv4_address: 172.29.101.{peer_ip}\n\n"


# test if created is correct
if __name__ == "__main__":

  created = peer_db_text(11, 1)

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
