#!/bin/bash
# start after update on rpg part of repo
now=$(date)
echo "$now --> RPG update > Starting..."
git -C /home/rjhadmin/tstsrv/ fetch origin
if  [ `git -C /home/rjhadmin/tstsrv/ rev-list HEAD...origin/main --count` != 0 ] 
then
    echo "$now --> RPG update > Remote git repo newer > Updating..."
    docker-compose --project-directory /home/rjhadmin/tstsrv/ stop rpg
    git -C /home/rjhadmin/tstsrv/ reset --hard origin/main
    git -C /home/rjhadmin/tstsrv/ fetch
    git -C /home/rjhadmin/tstsrv/ pull
    chmod +x /home/rjhadmin/tstsrv/*.sh
    docker-compose --project-directory /home/rjhadmin/tstsrv/ run rpg python rpg/manage.py makemigrations
    docker-compose --project-directory /home/rjhadmin/tstsrv/ run rpg python rpg/manage.py migrate
    docker-compose --project-directory /home/rjhadmin/tstsrv/ start rpg
    echo "$now --> RPG update > Update done!"
else
    echo "$now --> RPG update > Remote git repo same as local > Nothing to do!"
fi
echo "$now --> RPG update > Finished!"
