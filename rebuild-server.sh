#!/bin/bash
# stops docker-compose, reloads git repo, builds docker-compose fresh and restarts
git fetch origin
git reset --hard origin/main
git -C /home/rjhadmin/tstsrv/ fetch
git -C /home/rjhadmin/tstsrv/ pull
docker-compose --project-directory /home/rjhadmin/tstsrv/ down
# delete also all images
#docker rmi $(docker images -q) 
# reset even more docker files
#docker system prune -a --volumes

docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker-compose --project-directory /home/rjhadmin/tstsrv/ build --no-cache
docker-compose --project-directory /home/rjhadmin/tstsrv/ up -d



