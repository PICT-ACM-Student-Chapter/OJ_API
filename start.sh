#!/usr/bin/bash

# Start Judge0
echo 'Starting Judge0 Server'
docker compose -f docker-compose.judge0.yml up -d db redis
echo 'Waiting for 10 Seconds'
sleep 10s
docker compose -f docker-compose.judge0.yml up -d
echo 'Waiting for 5 Seconds'
sleep 5s

#Start Django Server
echo 'Starting Django Server'
docker compose up -d db-django
echo 'Waiting for 10 Seconds'
sleep 10s
docker compose up app
echo 'READY!!'
