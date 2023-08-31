from rest_framework import decorators, permissions, authentication, status
from rest_framework.response import Response
from . import models
import random, uuid


@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated])
@decorators.authentication_classes([authentication.BasicAuthentication]) # Not wantend
# @decorators.authentication_classes([authentication.TokenAuthentication]) # Wanted
def ProfileView ( request ) : 
    user = request.user

    leaders = models.LeaderboardModel.objects.all()[:5]
    ls = [{'username':i.user.username,'points':i.points} for i in leaders]
    

    userDetails = {
        'username' : user.username,
        'points' : models.LeaderboardModel.objects.get( user = user ).points
    }

    data = {
        'user' : userDetails,
        'leaders' : ls
    }

    return Response(data,status=status.HTTP_200_OK)



@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated])
@decorators.authentication_classes([authentication.BasicAuthentication]) # Not wantend
# @decorators.authentication_classes([authentication.TokenAuthentication]) # Wanted
def CreateSession(request) : 
    

    while True :
        ayah = random.choices(models.Ayah.objects.all())[0]
        
        if models.Ayah.objects.filter(text=ayah.text).count() == 1 :
            text = ayah.text
            surah = ayah.surah

            break
    
    all_choices = [
        random.choices(models.Surah.objects.all().exclude(surah_name=surah.surah_name))[0].surah_name,
        random.choices(models.Surah.objects.all().exclude(surah_name=surah.surah_name))[0].surah_name,
        random.choices(models.Surah.objects.all().exclude(surah_name=surah.surah_name))[0].surah_name,
        surah.surah_name
    ]

    
    random.shuffle(all_choices)
        
    choices = '@'.join(all_choices)

    s = models.SessionModel.objects.create(

        user = request.user,
        question = text,
        uuid = f'{uuid.uuid4()}',
        answers = choices,
        correct_answer = surah.surah_name,
        audio = ayah.audio
    )

    data = {
        'session':s.uuid
    }

    return Response(data,status=status.HTTP_201_CREATED)


def Questions (request) : 
    pass
