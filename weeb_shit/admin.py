from django.contrib import admin
from .models import fivestars, fourstars,threestars, twostars, onestars, list_of_anime, auto_complete, anime_database, Profile

# Register your models here.
admin.site.register(auto_complete)
admin.site.register(anime_database)
admin.site.register(Profile)
admin.site.register(fivestars)
admin.site.register(fourstars)
admin.site.register(threestars)
admin.site.register(twostars)
admin.site.register(onestars)