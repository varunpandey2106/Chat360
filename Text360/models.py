from django.db import models

# Create your models here.

from home.models import Profile

class Message(models.Model):
    body=models.TextField()
    sent_by= models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(Profile, blank=True,null=True , on_delete=models.SET_NULL)

    class Meta:
        ordering=('created_at',)
    
    def __str__(self):
        return f'{self.sent_by}'
    

class Room(models.Model):
    WAITING='waiting'
    ACTIVE='active'
    CLOSED= 'closed'

    CHOICES_STATUS=(
        (WAITING,'Waiting'),
        (ACTIVE,'Active'),
        (CLOSED,'Closed'),


    )

    uuid=models.CharField(max_length=300)
    client=models.CharField(max_length=300)
    agent=models.ForeignKey(Profile,related_name='rooms', blank= True,null=True,on_delete=models.SET_NULL)
    messages= models.ManyToManyField(Message, blank=True)
    url=models.CharField(max_length=300, blank=True,null=True)
    status=models.CharField(max_length=300,choices=CHOICES_STATUS,default=WAITING)
    created_at= models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering=('-created_at',)
    
    def __str__(self):
        return f'{self.client}-{self.uuid}'