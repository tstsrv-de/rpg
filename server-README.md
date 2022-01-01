# tst-srv.de Config README

Here is the config and some scripts for my 'Test Server' > tstsrv.de. Mainly in use for study related work and testing.

- Hosted @ hosteurope.de
- Domain @ inwx.de

Henning 'haenno' Beier, haenno@web.de, 24.11.2021


### Automate clone of git repo updates to container: 
Add a cron-job with the 'server-update-cron.sh' script: crontab -e, add the line: 
``*/5 * * * * /home/rjhadmin/tstsrv/server-update-cron.sh >> /home/rjhadmin/cronlog.txt 2>&1``
Dont forget to make the script executable with ``chmod +x server-update-cron.sh``!
