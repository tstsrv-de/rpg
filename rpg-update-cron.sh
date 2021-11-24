#!/bin/bash
# start after update on rpg part of repo
now=$(date "+%F %H:%M:%S")
# echo "$now --> RPG update > Starting..."
git -C /home/rjhadmin/tstsrv/ fetch origin >> /home/rjhadmin/cronlog.txt 
if  [ `git -C /home/rjhadmin/tstsrv/ rev-list HEAD...origin/main --count` != 0 ] 
then
    echo "$now --> RPG update > Remote git repo newer > Updating..."
    docker-compose --project-directory /home/rjhadmin/tstsrv/ stop rpg  >> /home/rjhadmin/cronlog.txt
    git -C /home/rjhadmin/tstsrv/ reset --hard origin/main  >> /home/rjhadmin/cronlog.txt
    git -C /home/rjhadmin/tstsrv/ fetch >> /home/rjhadmin/cronlog.txt
    git -C /home/rjhadmin/tstsrv/ pull >> /home/rjhadmin/cronlog.txt
    chmod +x /home/rjhadmin/tstsrv/*.sh >> /home/rjhadmin/cronlog.txt
    docker-compose --project-directory /home/rjhadmin/tstsrv/ run rpg python rpg/manage.py makemigrations >> /home/rjhadmin/cronlog.txt
    docker-compose --project-directory /home/rjhadmin/tstsrv/ run rpg python rpg/manage.py migrate >> /home/rjhadmin/cronlog.txt
    docker-compose --project-directory /home/rjhadmin/tstsrv/ start rpg >> /home/rjhadmin/cronlog.txt
    # echo "$now --> RPG update > Update done!"
else
    echo "$now --> RPG update > Remote git repo same as local > Nothing to do!"
fi
# echo "$now --> RPG update > Finished!"
