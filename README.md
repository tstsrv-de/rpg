# README for 'Browser RPG-Adventure'-project

## Short howto for local testing and/or dev useage

- Install git and docker

- Clone git repo to local system from <https://github.com/tstsrv-de/rpg>

- Change filename of ``example.env`` to ``.env`` in basedir <b><u>and</u></b> ``/rpg/rpg/``-folder

- Open a terminal, change directory to cloned git repo

- Run:

  ``docker-compose -f local-dev-docker-compose.yml build``

- Start the containers with:

  ``docker-compose -f local-dev-docker-compose.yml up -d``

- Apply updates on local db with:

  ``docker-compose -f local-dev-docker-compose.yml exec rpg python rpg/manage.py makemigrations``

  and:

  ``docker-compose -f local-dev-docker-compose.yml exec rpg python rpg/manage.py migrate``

- Restart container with:

  ``docker-compose -f local-dev-docker-compose.yml restart``

- Create local superuser with:

  ``docker-compose -f local-dev-docker-compose.yml exec rpg python rpg/manage.py createsuperuser``

- Load some sample-/base-data to database with:

  ``docker-compose -f local-dev-docker-compose.yml exec rpg python rpg/manage.py loaddata db_sample_data.json``

- Open and login to admin: <http://localhost:8000/admin> or open site itesef <http://localhost:8000/>
