# tst-srv.de Config README

Here is the config and some scripts for my 'Test Server' > tstsrv.de. Mainly in use for study related work and testing.

- Hosted @ hosteurope.de
- Domain @ inwx.de

Henning 'haenno' Beier, haenno@web.de, 24.11.2021







### Backup: Tips for local use on windows client with docker:

- Install git and docker
- Clone git repo to local windows system
- Change filename of ``local-win-.env`` to ``.env`` and copy it to the basefolder, /rpg/ and /rpg/rpg/
- Open cmd, cd into repo
- Run ``docker-compose -f local-win-docker-compose.yml build``
- Start the contains with ``docker-compose -f local-win-docker-compose.yml up -d``
- Apply updates on local db with ``docker-compose -f local-win-docker-compose.yml exec rpg python rpg/manage.py makemigrations`` and ``docker-compose -f local-win-docker-compose.yml exec rpg python rpg/manage.py migrate``
- Restart container with ``docker-compose -f local-win-docker-compose.yml restart``
- Create local superuser with ``docker-compose -f local-win-docker-compose.yml exec rpg python rpg/manage.py createsuperuser``
- Open and login to admin: http://localhost:8000/admin or open site itesef http://localhost:8000/