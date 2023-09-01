from django.shortcuts import render
from .serializers import LoginSerializer, RegisterSerializer
from django.contrib.auth.models import User
from rest_framework import mixins, generics
from rest_framework.response import Response
from rest_framework import status

class RegisterView ( generics.GenericAPIView, mixins.CreateModelMixin ) : 
    serializer_class = RegisterSerializer

    def post (self, request) : 

        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.get_token(),status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class LoginView ( generics.GenericAPIView, mixins.CreateModelMixin ) : 
    serializer_class = LoginSerializer

    def post (self, request) : 
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return Response(serializer.get_token(),status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
