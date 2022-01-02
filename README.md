# README for 'Browser RPG-Adventure'-project

## Short howto for local testing and/or dev useage

- Install git and docker
- Open a terminal, create an empty directory and change into it
- Clone git repo into the current directory with ``git clone git@github.com:tstsrv-de/rpg.git .``
- Copy *example.env* to *.env** in basedir with ``copy example.env .env`` or ``cp example.env .env``
- Also copy *rpg/rpg/example.env* to *rpg/rpg/.env* in *rpg/rpg/*-folder with ``copy rpg/rpg/example.env rpg/rpg/.env`` or ``cp rpg/rpg/example.env rpg/rpg/.env``
- Start building of the docker container:
  ``docker-compose -f local-dev-docker-compose.yml build``
- Start the containers with:
  ``docker-compose -f local-dev-docker-compose.yml up -d``
- Apply updates on local db with:
  ``docker-compose -f local-dev-docker-compose.yml exec rpg python rpg/manage.py makemigrations``
  and:
  ``docker-compose -f local-dev-docker-compose.yml exec rpg python rpg/manage.py migrate``
- Load some sample-/base-data to database with:
  ``docker-compose -f local-dev-docker-compose.yml exec rpg python rpg/manage.py loaddata db_sample_data.json``
- Restart container with:
  ``docker-compose -f local-dev-docker-compose.yml restart``
- Open site locally <http://localhost:8000/>

### Optional howto for use of Django admin

- Create local superuser with:
  ``docker-compose -f local-dev-docker-compose.yml exec rpg python rpg/manage.py createsuperuser``
- Open and login to admin: <http://localhost:8000/admin>
