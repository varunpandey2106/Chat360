from django.urls import path

from . import views

app_name='Text'

urlpatterns = [
    path('create-room/', views.create_room ,name='create-room'),
    path('api/getInitials/', views.get_initials, name='get_initials'),
    path('Text360-admin/', views.admin, name='admin'),
    


]
