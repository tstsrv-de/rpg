#!/bin/bash
# start after update on rpg part of repo
echo ' --> RPG update > Starting...'
git -C /home/rjhadmin/tstsrv/ fetch origin
if  [ `git -C /home/rjhadmin/tstsrv/ rev-list HEAD...origin/main --count` != 0 ] 
then
    echo ' --> RPG update > Remote git repo newer > Updating...'
    docker-compose --project-directory /home/rjhadmin/tstsrv/ stop rpg
    git -C /home/rjhadmin/tstsrv/ reset --hard origin/main
    git -C /home/rjhadmin/tstsrv/ fetch
    git -C /home/rjhadmin/tstsrv/ pull
    docker-compose --project-directory /home/rjhadmin/tstsrv/ run rpg python rpg/manage.py makemigrations
    docker-compose --project-directory /home/rjhadmin/tstsrv/ run rpg python rpg/manage.py migrate
    docker-compose --project-directory /home/rjhadmin/tstsrv/ start rpg
    echo ' --> RPG update > Update done!'
else
    echo ' --> RPG update > Remote git repo same as local > Nothing to do!'
fi
echo ' --> RPG update > Finished!'
