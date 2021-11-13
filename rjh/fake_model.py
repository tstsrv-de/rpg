import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fomtest.settings')

import django
django.setup()

import random
from myapp.models import Webpage, Topic, AccessRecord, User
from faker import Faker

fakegenerator = Faker()
topics = [
    'Online-Casino',
    'Social-Media',
    'Suchmaschinen',
    'Shops',
    'Games'
]

def add_topic():
    t = Topic.objects.get_or_create(name=random.choice(topics))[0]
    t.save()
    return t

def populate(N=5):
    for entry in range(N):
        top = add_topic()
        url = fakegenerator.url()
        created_at = fakegenerator.date()
        name = fakegenerator.company()

        wp = Webpage.objects.get_or_create(topic=top, url=url, name=name, created_at=created_at)[0]
        ar = AccessRecord.objects.get_or_create(name=wp, date=created_at)[0]

        wp.save()
        ar.save()

def populate_users(N=5):
    for entry in range(N):
        first_name = fakegenerator.first_name()
        last_name = fakegenerator.last_name()
        email = fakegenerator.email()

        u = User.objects.get_or_create(first_name=first_name, last_name=last_name, email=email)[0]
        u.save()
        
if __name__ == '__main__':
    print("Generate data ....")
    #populate(100)
    populate_users(100)
    print("Data generated!")