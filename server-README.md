# tst-srv.de Config README

Here is the config and some scripts for my 'Test Server' > tstsrv.de. Mainly in use for study related work and testing.

- Hosted @ hosteurope.de
- Domain @ inwx.de

Henning 'haenno' Beier, haenno@web.de, 24.11.2021

## Automation of git repo updates to this servers containers

With the 'server-update-cron.sh' script in the <b>crontab</b> as...
``*/5 * * * * /home/rjhadmin/tstsrv/server-update-cron.sh >> /home/rjhadmin/cronlog.txt 2>&1``

...this server automaticly pulls each new commit to this repo, and restarts the docker containers.

Note that there are two different ``Dockerfiles`` and ``docker-compose.yml`` in this repo. This allows to keep the server updated and also runnig a local dev-/testing-installation.

The online variant runs without the set debug-flag in the ``.env`` files and a traefic reverse proxy with https/letsencrypt. 
