#!/bin/bash
# stops docker-compose, reloads git repo, builds docker-compose fresh and restarts

git fetch origin
git reset --hard origin/main
git -C /home/rjhadmin/tstsrv/ fetch
git -C /home/rjhadmin/tstsrv/ pull
docker-compose --project-directory /home/rjhadmin/tstsrv/ down

# optional: delete also all images and prune local-data, then build with no-cache 
#docker rmi $(docker images -q) 
#docker system prune -a --volumes
#docker stop $(docker ps -a -q)
#docker rm $(docker ps -a -q)
#docker-compose --project-directory /home/rjhadmin/tstsrv/ build --no-cache

docker-compose --project-directory /home/rjhadmin/tstsrv/ build 
docker-compose --project-directory /home/rjhadmin/tstsrv/ up -d
docker-compose --project-directory /home/rjhadmin/tstsrv/ exec rpg python rpg/manage.py makemigrations
docker-compose --project-directory /home/rjhadmin/tstsrv/ exec rpg python rpg/manage.py migrate 
docker-compose --project-directory /home/rjhadmin/tstsrv/ exec rpg python rpg/manage.py loaddata db_sample_data.json 
    
chmod +x /home/rjhadmin/tstsrv/*.sh
