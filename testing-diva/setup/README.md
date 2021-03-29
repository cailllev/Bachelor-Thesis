# DIVA.EXCHANGE "Dockerized"

This project has the following purpose: even if DIVA.EXCHANGE consists of several independent modules, it still should be easy to have the complete environment available.

Online Demo and Test sites:
* https://testnet.diva.exchange - The public DIVA.EXCHANGE testnet. Everybody can join.

It's licenced under [AGPLv3](LICENSE).

## Automatic Setup

Running the following command creates a local testnet with a variable number of nodes.
```
python3 setup.py <nr of nodes>
```
With this setup, some of the api adresses change due to more nodes and hence more addresses used.
```
Explorer:	172.29.101.100:3920 (no change)
API:		172.29.101.30:19012 (no change)
Torii:		172.29.101.12:50051 (#changed#, takes the ip addr of first node if not already defined in ENV)
```

## Manual Setup


Clone the code repository from the public repository:
```
git clone -b develop https://codeberg.org/diva.exchange/diva-dockerized.git
cd diva-dockerized
```

To start the local testnet (7 nodes) execute:
```
sudo docker-compose -f docker-compose/local-testnet.yml pull && sudo docker-compose -f docker-compose/local-testnet.yml up -d
```

To stop the local testnet execute:
```
sudo docker-compose -f docker-compose/local-testnet.yml down --volumes
```

## Donations

Your donation goes entirely to the project. Your donation makes the development of DIVA.EXCHANGE faster.

XMR: 42QLvHvkc9bahHadQfEzuJJx4ZHnGhQzBXa8C9H3c472diEvVRzevwpN7VAUpCPePCiDhehH4BAWh8kYicoSxpusMmhfwgx

BTC: 3Ebuzhsbs6DrUQuwvMu722LhD8cNfhG1gs

Awesome, thank you!

## License

[AGPLv3](LICENSE)
