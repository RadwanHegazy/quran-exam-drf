from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token



class RegisterSerializer ( serializers.ModelSerializer ) : 
    class Meta : 
        model = User
        fields = ['username','email','password']

    def create(self, validated_data):
        
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create_user( 
            username = username,
            email = email,
            password = password,
         )
        
        user.save()

        self.token = {'token': Token.objects.get( user = user ).key }

        return user

    def get_token (self) : 
        return self.token



class LoginSerializer ( serializers.ModelSerializer ) : 
    class Meta : 
        model = User
        fields = ['email','password']


    def validate(self, data):
        
        email = data['email']
        password = data['password']

        user = User.objects.filter( email = email )

        if user.count() != 1 : 
            raise serializers.ValidationError('Invalid Email')
        
        user = user.first()

        if not user.check_password(password) : 
            raise serializers.ValidationError('Invalid Password')


        self.token = {'token':Token.objects.get( user = user ).key}
        
        return data
    
    def get_token (self) : 
        return self.token
    