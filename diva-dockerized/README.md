 DIVA.EXCHANGE "Dockerized"

This project has the following purpose: even if DIVA.EXCHANGE consists of several independent modules, it still should be easy to have the complete environment available.

Online Demo and Test sites:
* https://testnet.diva.exchange - The public DIVA.EXCHANGE testnet. Everybody can join.

It's licenced under [AGPLv3](LICENSE).


## Get Started

**IMPORTANT**: To start a local Iroha testnet, make sure you have [Docker Compose](https://docs.docker.com/compose/install/) installed. Check your Docker Compose installation by executing `docker-compose --version` in a terminal.

Clone the code repository from the public repository:
```
git clone -b master https://codeberg.org/diva.exchange/BA2021-Cailllev-Kybursas
cd BA2021-Cailllev-Kybursas/diva-dockerized
```

To start the local testnet (7 nodes) execute:
```
sudo docker-compose -f docker-compose/local-testnet.yml pull && sudo docker-compose -f docker-compose/local-testnet.yml up -d
```

To stop the local testnet execute:
```
sudo docker-compose -f docker-compose/local-testnet.yml down --volumes
```

Open your browser and take a look at your local testnet using the Iroha Blockchain Explorer: http://172.29.101.100:3920 or the DIVA API Endpoint: http://172.29.101.30:19012/accounts. Remark: it takes a few seconds to tart the docker container which contains the explorer.

## Contact the Developers

On [DIVA.EXCHANGE](https://www.diva.exchange) you'll find various options to get in touch with the team.

Talk to us via Telegram [https://t.me/diva_exchange_chat_de]() (English or German).

## Donations

Your donation goes entirely to the project. Your donation makes the development of DIVA.EXCHANGE faster.

XMR: 42QLvHvkc9bahHadQfEzuJJx4ZHnGhQzBXa8C9H3c472diEvVRzevwpN7VAUpCPePCiDhehH4BAWh8kYicoSxpusMmhfwgx

BTC: 3Ebuzhsbs6DrUQuwvMu722LhD8cNfhG1gs

Awesome, thank you!

## License

[AGPLv3](LICENSE)
