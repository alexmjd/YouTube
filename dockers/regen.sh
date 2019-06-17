#!/bin/bash

docker stop t_python t_encoder #t_db
docker rm t_python t_encoder #t_db
#docker rmi encodocker
docker-compose up -d