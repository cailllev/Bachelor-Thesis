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
Explorer:	172.29.101.252:3920
API:		172.29.101.254:19012
Torii:		172.29.101.253:50051 (if not defined in ENV)

old:
Explorer:	172.29.101.100:3920
API:		172.29.101.30:19012
Torii:		172.29.101.21:50051 (if not defined in ENV)

## Manual Setup

### Docker Compose & Clone the Code

**IMPORTANT**: To start a local Iroha testnet, make sure you have [Docker Compose](https://docs.docker.com/compose/install/) installed. Check your Docker Compose installation by executing `docker-compose --version` in a terminal.

Clone the code repository from the public repository:
```
git clone -b master https://codeberg.org/diva.exchange/diva-dockerized.git
cd diva-dockerized
```

## Donations

Your donation goes entirely to the project. Your donation makes the development of DIVA.EXCHANGE faster.

XMR: 42QLvHvkc9bahHadQfEzuJJx4ZHnGhQzBXa8C9H3c472diEvVRzevwpN7VAUpCPePCiDhehH4BAWh8kYicoSxpusMmhfwgx

BTC: 3Ebuzhsbs6DrUQuwvMu722LhD8cNfhG1gs

Awesome, thank you!

## License

[AGPLv3](LICENSE)
