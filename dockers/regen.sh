#!/bin/bash

docker stop t_python t_encoder t_node #t_db
docker rm t_python t_encoder t_node #t_db
#docker rmi encodocker
docker rmi nodocker
docker-compose up -d