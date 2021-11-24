#!/bin/bash
# start after update on rpg part of repo

git fetch origin
git reset --hard origin/main
git -C /home/rjhadmin/tstsrv/ fetch
git -C /home/rjhadmin/tstsrv/ pull

docker-compose stop rpg
docker-compose run rpg python rpg/manage.py makemigrations
docker-compose run rpg python rpg/manage.py migrate
docker-compose start rpg
