from django.urls import path

from . import views

app_name='Text'

urlpatterns = [
    path('create-room/', views.create_room ,name='create-room')
]
