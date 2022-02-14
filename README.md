# README for 'Browser RPG-Adventure'-project

This is the code and documentation for "Browser RPG-Adventure"-project (as part of an examination in the 5th semester of business informatics, FOM University of Siegen).

The final product, the game **MONSTER SLAYER**, can be found and played at <https://rpg.tstsrv.de>.

The authors are:
- Frakes95 <https://github.com/Frakes95>
- haenno <https://github.com/haenno>
- derBart0815 <https://github.com/derBart0815>

## Credits and acknowledgements

- Ronen Ness for a CSS-Framework <https://github.com/RonenNess/RPGUI>
- A Django Chat-Tutorial <https://github.com/veryacademy/YT-Django-Project-Chatroom-Getting-Started>
- The Krita manual <https://docs.krita.org/en/index.html>
- Igor Bubelov for a Traefik guide  <https://github.com/bubelov/traefik-letsencrypt-compose>

## Short howto for local testing and/or dev useage

- Install git and docker
- Open a terminal, create an empty directory and change into it
- Clone git repo into the current directory with ``git clone git@github.com:tstsrv-de/rpg.git .``
- Copy *example.env* to *.env** in basedir with  ``copy example.env .env`` (on 🪟) or ``cp example.env .env`` (on 🍎 and 🐧)
- Also copy *rpg/rpg/example.env* to *rpg/rpg/.env* in *rpg/rpg/*-folder with ``copy "rpg/rpg/example.env" "rpg/rpg/.env"`` (on 🪟) or ``cp rpg/rpg/example.env rpg/rpg/.env`` (on 🍎 and 🐧)
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

### Scripts for following usage 

If you want to keep using this local *installation*, just use on of the scripts ``local-dev-start.bat`` (on 🪟)  or ``local-dev-start.sh``  (on 🍎 and 🐧) to start it back up again. On each start they will collect and apply migrations, load sample data to the database from the *.json file in the base-dir and start the docker containers (Django server and the database) back up again. Also it will keep the terminal open, so that you can see all the (error-)messages and output from Django and the database.

## Licence

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
