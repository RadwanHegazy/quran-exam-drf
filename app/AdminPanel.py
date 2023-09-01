from django.contrib.admin import ModelAdmin
from . import models



class SurahPanel ( ModelAdmin ) : 
    list_display = ['surah_name','surah_type','number_of_ayahs']


class AyahPanel ( ModelAdmin ) :
    list_display = ['surah','number']

class LeaderboardPanel ( ModelAdmin ) : 
    list_display = ['user','points']

class SessionPanel ( ModelAdmin ) : 
    list_display = ['user','uuid']