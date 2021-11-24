#!/bin/bash
# start after update on rpg part of repo
echo ' --> RPG update > Starting...'
git fetch origin
if  [ `git rev-list HEAD...origin/main --count` != 0 ] 
then
    echo ' --> RPG update > Remote git repo newer > Updating...'
    docker-compose stop rpg
    git reset --hard origin/main
    git -C /home/rjhadmin/tstsrv/ fetch
    git -C /home/rjhadmin/tstsrv/ pull
    docker-compose run rpg python rpg/manage.py makemigrations
    docker-compose run rpg python rpg/manage.py migrate
    docker-compose start rpg
    echo ' --> RPG update > Update done!'
else
    echo ' --> RPG update > Remote git repo same as local > Nothing to do!'
fi
echo ' --> RPG update > Finished!'