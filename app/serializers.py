from rest_framework import serializers
from . import models
from django.shortcuts import get_object_or_404
import random, uuid as my_uuid

class SessionSerializer ( serializers.ModelSerializer ) : 
    user_answer = serializers.CharField(write_only=True)
    uuid = serializers.CharField(write_only=True)
    class Meta : 
        fields = ('user_answer','uuid')
        model = models.SessionModel

    


    def get_data ( self , session, user) :
        
        data = {
            
            'session':{
                'uuid' : session.uuid,
                'text' : session.question,
                'choices' : session.answers.split('@') ,
                'user_answer' : session.user_answer,
                'audio' : session.audio,
            },

            'user' : {
              'username': user.username,
              'points' : models.LeaderboardModel.objects.get(user=user).points,  
            }

        }

        return data

    def validate ( self , data) : 
        user_answer = data['user_answer']
        uuid = data['uuid']

        session = get_object_or_404(models.SessionModel, uuid = uuid)

        if user_answer not in session.answers.split('@') :
            raise serializers.ValidationError('Invalid Data')
        
        return  data

    def check_answer ( self, session, user_answer ) : 
        
        if session.user_answer : 
            raise serializers.ValidationError('Session Expired')

        session.user_answer = user_answer
        session.save()

        points = models.LeaderboardModel.objects.get(user=session.user)

        data = {
            'isCorrect' : False,
            'points' : points.points
        }

        if session.correct_answer == user_answer :
            points.points = points.points + 5
            points.save()

            data['isCorrect'] = True
            data['points'] = points.points


        return data
    




class GenerateSessionSerializer ( serializers.ModelSerializer ) : 
    uuid = serializers.CharField(read_only=True)
    class Meta :
        fields = ('uuid',)
        model = models.SessionModel
    
    def create_session ( self, user ) :

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

            user = user,
            question = text,
            uuid = f'{my_uuid.uuid4()}',
            answers = choices,
            correct_answer = surah.surah_name,
            audio = ayah.audio
        )

        data = {
            'session':s.uuid
        }

        return data
    