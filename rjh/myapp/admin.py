from django.contrib import admin

from myapp.models import Webpage, Topic, User, AccessRecord

admin.site.register(Webpage)
admin.site.register(Topic)
admin.site.register(User)
admin.site.register(AccessRecord)