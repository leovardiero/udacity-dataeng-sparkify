set -e  #fail fast

echo "Reading values from docker-compose..."
CASSANDRA_VERSION=`docker-compose config | grep 'image:.*cassandra:' | head -1 | awk -F":" '{ print $NF}'`
docker image pull cassandra:${CASSANDRA_VERSION}

echo "Echo reading standart configuration..."
docker run --rm -d --name tmp cassandra:${CASSANDRA_VERSION}
docker cp tmp:/etc/cassandra/ etc_cassandra_${CASSANDRA_VERSION}_vanilla/
docker stop tmp

echo "Creating folders..."
etc_volumes=`docker-compose config | grep '/etc/cassandra' | awk -F ":" '{ print $1}' | awk '{ print $NF}'`
for v in ${etc_volumes}; do
   mkdir -p ${v}
   cp -r etc_cassandra_${CASSANDRA_VERSION}_vanilla/*.* ${v}/
done

echo "Starting cluster..."
docker-compose up
