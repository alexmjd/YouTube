#!/bin/bash

docker stop t_python t_encoder #t_db
docker rm t_python t_encoder #t_db
docker-compose up -d