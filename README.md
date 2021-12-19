# tst-srv.de Config README

Here is the config and some scripts for my 'Test Server' > tstsrv.de. Mainly in use for study related work and testing.

- Hosted @ hosteurope.de
- Domain @ inwx.de

Henning 'haenno' Beier, haenno@web.de, 24.11.2021



# README for 'Browser RPG-Adventure' (Rico, Julian, Henning)

## Tips for local use on windows client with docker:

- Install git and docker
- Clone git repo to local windows system
- Change filename of ``local-win-.env`` to ``.env`` and copy it to the basefolder, /rpg/ and /rpg/rpg/
- Open cmd, cd into repo
- Run ``docker-compose -f local-win-docker-compose.yml build``
- Start the containers with ``docker-compose -f local-win-docker-compose.yml up -d``
- Apply updates on local db with ``docker-compose -f local-win-docker-compose.yml exec rpg python rpg/manage.py makemigrations`` and ``docker-compose -f local-win-docker-compose.yml exec rpg python rpg/manage.py migrate``
- Restart container with ``docker-compose -f local-win-docker-compose.yml restart``
- Create local superuser with ``docker-compose -f local-win-docker-compose.yml exec rpg python rpg/manage.py createsuperuser``
- Open and login to admin: http://localhost:8000/admin or open site itesef http://localhost:8000/


## Todo: 
- Add license 
- Configure e-mail service



## Project dev documentation: 

### Add user registration & more:
See https://www.nintyzeros.com/2020/06/login-register-user%20page-in%20django.html

See https://docs.djangoproject.com/en/3.2/topics/auth/default/#built-in-auth-forms
New URLs:
        accounts/login/ [name='login']
        accounts/logout/ [name='logout']
        accounts/password_change/ [name='password_change']
        accounts/password_change/done/ [name='password_change_done']
        accounts/password_reset/ [name='password_reset']
        accounts/password_reset/done/ [name='password_reset_done']
        accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
        accounts/reset/done/ [name='password_reset_complete']

### Added bootstrap
See https://www.w3schools.com/bootstrap/bootstrap_navbar.asp

## Project use documentation: 

### On update of rpg git repo:
Run the script "only-rebuild-rpg.sh". It will get the new files and changes from the git repo, stops the container, runs django updates in container and starts the container again.

### Automate clone of git repo updates to container: 
Add a cron-job with the 'rpg-update-cron.sh' script: crontab -e, add the line: 
``*/5 * * * * /home/rjhadmin/tstsrv/rpg-update-cron.sh >> /home/rjhadmin/cronlog.txt 2>&1``
And make the script executable with chmod +x!

## Project setup documentation: 
Init: 
1. copy files (docker-compose, dockerfile, example.env, requirements.txt) from repo local
2. rename .env.example to .env and change settings 
3. init django with: docker-compose run rpg django-admin startproject rpg .
4. edit rpg/settings.py:
    add:
        start:
            import os
            import environ
            env = environ.Env()
            environ.Env.read_env()
        after 'BASE_DIR':
            TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
            STATIC_DIR = os.path.join(BASE_DIR, 'static')
        after STATIC_URL:
            STATICFILES_DIRS = [
                STATIC_DIR,
            ]
    change: 
        SECRET_KEY to:
            SECRET_KEY = env('ENV_SECRET_KEY')
        ALLOWED_HOSTS to:
            ALLOWED_HOSTS = [env('ENV_ALLOWED_HOSTS')]
        in Templates, Dirs to:
                'DIRS': [TEMPLATES_DIR],
        DATABASES to:
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': env('ENV_POSTGRES_DB'),
                    'USER': env('ENV_POSTGRES_USER'),
                    'PASSWORD': env('ENV_POSTGRES_PASSWORD'),
                }
            }

5. copy and rename .env.example also to rpg/.env (remeber to copy again @changes)
6. update django to new db: 'docker-compose run python manage.py makemigrations' and 'docker-compose run python manage.py migrate'
7. create superuser: docker-compose run rpg python manage.py createsuperuser
8. create django app: docker-compose run rpg python manage.py startapp rjh_rpg 


