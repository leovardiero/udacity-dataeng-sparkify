import yaml
import json
import os
from distutils.dir_util import copy_tree

#****************************************************************
#                                                            YAML
#****************************************************************

def getEtcVolumes():
  etc_volumes = []
  with open('docker-compose.yml') as file:
    document = yaml.full_load(file)
    
    for container in document['services']:
      volumes = document['services'][container]['volumes']
      for volume in volumes:
        if ('/etc/cassandra' in volume):
          etc_volumes.append(volume.split(':')[0])

  return etc_volumes

def getCassandraVersion():
  with open('docker-compose.yml') as file:
    document = yaml.full_load(file)


#****************************************************************
#                                                       CONTAINER
#****************************************************************

def getStandardConfiguration():
  os.system('docker run --rm -d --name tmp cassandra:3.11.8')
  os.system('docker cp tmp:/etc/cassandra/ etc_cassandra_3.11.8_vanilla/')
  os.system('docker stop tmp')

def startCompose():
  os.system('docker-compose up')

#****************************************************************
#                                                            MAIN
#****************************************************************

def main():
  print('Get configuration from tmp container')
  getStandardConfiguration()


  print('Create folders and copy')
  os.mkdir('etc')
  for etc in getEtcVolumes():
    if (not os.path.exists(etc)):
      os.mkdir(etc)
    copy_tree('etc_cassandra_3.11.8_vanilla/', etc)

  startCompose()

if __name__ == '__main__':
  main()

        

      