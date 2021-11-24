# README for 'Browser RPG-Adventure' (Rico, Julian, Henning)

## foo bar wiz
Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Todo: 
- Add license 

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

