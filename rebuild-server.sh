#!/bin/bash
# stops docker-compose, reloads git repo, builds docker-compose fresh and restarts
git -C /home/rjhadmin/tstsrv/ fetch
git -C /home/rjhadmin/tstsrv/ pull
docker-compose --project-directory /home/rjhadmin/tstsrv/ down
docker-compose --project-directory /home/rjhadmin/tstsrv/ build
docker-compose --project-directory /home/rjhadmin/tstsrv/ up -d



