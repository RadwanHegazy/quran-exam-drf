from rest_framework import decorators, generics,permissions, authentication, status
from rest_framework.response import Response
from . import models
from django.shortcuts import get_object_or_404
from .serializers import SessionSerializer, GenerateSessionSerializer

@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated])
@decorators.authentication_classes([authentication.TokenAuthentication]) # Wanted
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




class GenerateSessionView ( generics.GenericAPIView ) : 
    serializer_class = GenerateSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post (self, request) : 
        serializer = self.serializer_class()
        data = serializer.create_session( user = request.user )
        
        return Response(data,status=status.HTTP_201_CREATED) 





class Questions ( generics.GenericAPIView) :
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [ authentication.TokenAuthentication ]

    def get ( self, request, sessionid ) : 

        
        session = get_object_or_404( models.SessionModel, uuid = sessionid )
        
        if session.user_answer or session.user != request.user : 
            return Response(status=status.HTTP_404_NOT_FOUND)
 

        user = request.user

        readable_data = self.serializer_class()
        readable_data = readable_data.get_data(session, user)

        return Response(data=readable_data,status=status.HTTP_200_OK)

    def post ( self, request ,sessionid ) :
        
        
        session = get_object_or_404( models.SessionModel ,uuid = sessionid )
        
                
        if session.user_answer or session.user != request.user : 
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid() : 
            data = serializer.check_answer( session = session, user_answer = serializer.validated_data['user_answer'] )
            return Response(data = data)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

