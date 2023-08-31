from django.urls import path
from . import views


urlpatterns = [
    path('',views.ProfileView),
    path('session/',views.CreateSession),
    
]