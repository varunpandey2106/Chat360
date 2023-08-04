from django.db import models

# Create your models here.

class friendVCmember(models.Model):
    name= models.CharField(max_length=200)
    uid=models.CharField(max_length=1000)
    friendVCname=models.CharField(max_length=200)
    insession= models.BooleanField(default=True)

    def __str__(self):
        return self.name
