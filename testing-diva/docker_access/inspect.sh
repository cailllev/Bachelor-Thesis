# start container
sudo docker-compose -f setup_iroha.yml up -d

# inspect rights via container
printf "\nvia docker exec"
printf "\n***************"

printf "\n/data\n"
sudo docker exec -it n1.testnet.diva.local bash -c "ls -alh data"

printf "\n/data/local-genesis\n"
sudo docker exec -it n1.testnet.diva.local bash -c "ls -alh data/local-genesis"

printf "\n/data/testnet.diva.i2p\n"
sudo docker exec -it n1.testnet.diva.local bash -c "ls -alh data/testnet.diva.i2p"

printf "\n/blockstore\n"
sudo docker exec -it n1.testnet.diva.local bash -c "ls -alh blockstore"


# inspect rights via host
path="/var/lib/docker/volumes/n1.testnet.diva.local/_data"
printf "\nvia host\n"
printf "***************"

printf "\n/data\n"
sudo ls -alh $path"/data"

printf "\n/data/local-genesis\n"
sudo ls -alh $path"/data/local-genesis"

printf "\n/data/testnet.diva.i2p\n"
sudo ls -alh $path"/data/testnet.diva.i2p"

printf "\n/blockstore\n"
sudo ls -alh $path"/blockstore"
printf "\n"

sudo docker-compose -f setup_iroha.yml down --volumes



# access via host
# ***************

# normal user
# -----------
# $ cat /var/lib/docker/volumes/n1.testnet.diva.local/_data/data/n1.priv
# cat: /var/lib/docker/volumes/n1.testnet.diva.local/_data/data/n1.priv: Permission denied

# root
# ----
# sudo cat /var/lib/docker/volumes/n1.testnet.diva.local/_data/data/n1.priv
# 16ba05b4b39bac3c81a7e7a132dd554a64b330d9ab840b6ad51a7b46214bc173



# access via docker exec
# **********************

# normal user
# -----------
# $ docker exec -it n1.testnet.diva.local bash -c "cat data/n1.priv"
# Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get http://%2Fvar%2Frun%2Fdocker.sock/v1.24/containers/n1.testnet.diva.local/json: dial unix /var/run/docker.sock: connect: permission denied

# root
# ----
# $ sudo docker exec -it n1.testnet.diva.local bash -c "cat data/n1.priv"
# 16ba05b4b39bac3c81a7e7a132dd554a64b330d9ab840b6ad51a7b46214bc173


# conclusion
# **********
# Altough the access rights of the files are: 
# -rw-rw-r-- 1 root root   64 Apr  1 04:40 n1.priv
# "docker exec" is only excecutable by root and the folder "/var/lib/docker" is only readable and writeable by root:
# $ ls -alh /var/lib/ | grep docker
# drwx--x--x 14 root          root          4.0K May 13 04:47 docker

# Contents of the docker folder would still be executable, but the folder /var/lib/docker is marked as non executable:
# $ sudo ls -alh /var/lib/docker | grep volumes
# drwx------  3 root root  12K May 13 05:16 volumes

# Additionally, there are no executable files in the docker container nor set UID binaries, so the keys are protected as well as it's possible.
