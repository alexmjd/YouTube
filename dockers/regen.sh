#!/bin/bash

docker stop t_python t_encoder t_node t_mailer t_rabbit #t_db
docker rm t_python t_encoder t_node t_mailer t_rabbit #t_db
docker-compose up -d #--build --force-recreate