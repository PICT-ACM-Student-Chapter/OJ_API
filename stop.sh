#!/usr/bin/bash

# Stop Judge0
docker-compose -f docker-compose.judge0.yml down

#Stop Django
docker-compose down
