import yaml
import json
import os
import sys
import subprocess
import docker
import time
from distutils.dir_util import copy_tree
from shutil import rmtree


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

  image = document['services']['cass1']['image']
  version = image.split(':')[1]

  return version

def getContainers():
  with open('docker-compose.yml') as file:
    document = yaml.full_load(file)

  return document['services'].keys()


#****************************************************************
#                                                       CONTAINER
#****************************************************************

def getStandardConfiguration():
  version = getCassandraVersion()

  try:
    os.system(f'docker run --rm -d --name tmp cassandra:{version}')
    os.system(f'docker cp tmp:/etc/cassandra/ etc_cassandra_{version}_vanilla/')
    os.system('docker stop tmp')
  except Exception as e:
    print(e)
    sys.exit(1)

def startCompose():
  try:
    subprocess.check_output('docker-compose up -d', shell=True)
  except Exception as e:
    print(e)
    sys.exit(1)

#****************************************************************
#                                                            MAIN
#****************************************************************

def main():
  version = getCassandraVersion()
  print('Get configuration from tmp container')
  getStandardConfiguration()


  print('Create folders and copy')
  if (not(os.path.exists('etc'))):
    os.mkdir('etc')
  for etc in getEtcVolumes():
    if (not(os.path.exists(etc))):
      os.mkdir(etc)
    copy_tree(f'etc_cassandra_{version}_vanilla/', etc)

  startCompose()
  time.sleep(15)

  docker_client = docker.from_env()
  while True:
    i = 0
    for container in docker_client.containers.list(all = True):
      if (container.attrs['State']['Status'] == 'running'):
        i = i + 1

    if (i == 3):
      break

    print('Waiting all containers run')
    time.sleep(3)


  rmtree('etc')
  rmtree(f'etc_cassandra_{version}_vanilla/')

if __name__ == '__main__':
  main()

        

      