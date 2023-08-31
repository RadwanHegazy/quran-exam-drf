from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer ( serializers.ModelSerializer ) : 
    class Meta : 
        model = User
        fields = ['username','email','password']

    # create validation for registeration
    def create(self, validated_data):
        # return super().create(validated_data)
        pass    

class LoginSerializer ( serializers.ModelSerializer ) : 
    class Meta : 
        model = User
        fields = ['email','password']


    # create validation for login
    def create(self, validated_data):
        # return super().create(validated_data)
        pass