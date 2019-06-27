#!/bin/bash

docker stop t_python t_encoder t_node t_mailer t_rabbit #t_db
docker rm t_python t_encoder t_node t_mailer t_rabbit #t_db
#docker rmi encodocker
#docker rmi nodocker
#docker rmi mailocker
#docker rmi rabbitocker
docker-compose up -d
