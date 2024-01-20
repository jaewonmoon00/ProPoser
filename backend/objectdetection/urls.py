from django.urls import path
from . import views

urlpatterns = [
    path('video_feed/', views.stream_video, name='video_feed'),
    path('result/', views.get_poses, name='result')
]