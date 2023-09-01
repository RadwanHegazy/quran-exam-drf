from django.urls import path
from . import views


urlpatterns = [
    path('',views.ProfileView),
    path('session/',views.GenerateSessionView.as_view()),
    path('q/<str:sessionid>/',views.Questions.as_view()),

]