from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save



@receiver(post_save, sender = User)
def CreateToken ( created, instance, **args ) : 
    if created : 
        Token.objects.create( user = instance )