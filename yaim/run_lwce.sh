#!/bin/bash

declare -a NODES
NODE_INDEX=0
HOST=$(hostname -f)
DOCKER_RUN="sudo docker run "
declare -a PORTS=('8443' '2811' '20000-21000' '49152' '49155' '49154' '9002' '9001' '3306' '2170' '33333' '56565' '56554')
for i in "$@"
do
case $i in
    --ip=*)
	IP="${i#*=}"
	shift
	;;
	--net=*)
	NET="${i#*=}"
	shift
	;;
	--config=*)
	CONFIG="${i#*=}"
	shift
	;;
	--node=*)
	NODES[NODE_INDEX]="${i#*=}"
	NODE_INDEX=$((NODE_INDEX + 1))
	shift
	;;
	-h|--help)
	echo "Usage:"
	echo "run_lwce.ch [--ip=<value>] [--host=<value>] [--net=<overlay_network_name>] [--config=<ce-config_path>] [[--node=<hostname:ip>] [--node=<hostname:ip>] ...]"
	printf "\n"
	echo "Options:"
	echo "1. ip: REQUIRED; The IP address to be assigned to the container."
	echo "2. net: REQUIRED; The name of the attachable overlay network to which the container should attach on startup. You should already have created an attachable overlay network on your swarm manager."
	echo "3. node: OPTIONAL; HOSTNAME:IP of other nodes on the same docker swarm network. The /etc/hosts inside the current container is appended with this info."
	exit 0
	shift
	;;
esac
done
if [ -z "$IP" ]
then
	echo "Please specify the ip address for the cream container. It should be in the same subnet as the docker overlay network that connects all other containers."
	exit 1
elif [ -z "$NET" ]
then
	echo "Please specify the name of the attachable docker overlay network that the container should connect to on startup."
	exit 1
fi
if [ $NODE_INDEX -eq 0 ]
then
	echo "Please note that no additional nodes have been specified. Therefore the /etc/hosts file in the container won't be modified. This could potentially create some troubles when trying to communicate over the overlay network."
	sleep 5
fi
echo "Starting container..."
echo "IP = ${IP}"
echo "HOST = ${HOST}"
echo "NET = ${NET}"
echo "CONFIG = ${CONFIG}"
for NODE in ${NODES[@]}; do
	echo "NODE = $NODE"
done


echo "${DOCKER_RUN}"
DOCKER_RUN="$DOCKER_RUN -itd -d"
DOCKER_RUN="$DOCKER_RUN --name ${HOST}"
DOCKER_RUN="$DOCKER_RUN --net ${NET}"
DOCKER_RUN="$DOCKER_RUN --ip ${IP}"
DOCKER_RUN="$DOCKER_RUN --hostname ${HOST}"
for NODE in ${NODES[@]}; do
    DOCKER_RUN="$DOCKER_RUN --add-host ${NODE}"
done
for PORT in ${PORTS[@]}; do
    DOCKER_RUN="$DOCKER_RUN -p $PORT:$PORT"
done
DOCKER_RUN="$DOCKER_RUN --privileged"
#DOCKER_RUN="$DOCKER_RUN --mount type=bind,source="$(pwd)"/ce-config,target=/ce-config"
DOCKER_RUN="$DOCKER_RUN --mount type=bind,source="${CONFIG}",target=/ce-config"
DOCKER_RUN="$DOCKER_RUN maany/lwce-umd4 /bin/bash"

echo "The following docker command will be executed:"
echo $DOCKER_RUN

$DOCKER_RUN
sudo docker exec -it ${HOST} /ce-config/init.sh
