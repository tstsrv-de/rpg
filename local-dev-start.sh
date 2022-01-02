#!/bin/bash
docker-compose -f local-dev-docker-compose.yml up -d
docker-compose -f local-dev-docker-compose.yml exec rpg python rpg/manage.py makemigrations
docker-compose -f local-dev-docker-compose.yml exec rpg python rpg/manage.py migrate
docker-compose -f local-dev-docker-compose.yml exec rpg python rpg/manage.py loaddata db_sample_data.json
docker-compose -f local-dev-docker-compose.yml stop
docker-compose -f local-dev-docker-compose.yml up
