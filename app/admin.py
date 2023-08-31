from django.contrib import admin
from . import models
from django.contrib.auth.models import Group
from . import AdminPanel




# add models to admin panel
admin.site.register( models.Surah, AdminPanel.SurahPanel )
admin.site.register( models.Ayah , AdminPanel.AyahPanel)
admin.site.register( models.LeaderboardModel , AdminPanel.LeaderboardPanel)
admin.site.register( models.SessionModel , AdminPanel.SessionPanel)




# remove Group Model
admin.site.unregister(Group)


