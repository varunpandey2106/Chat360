from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    image=models.ImageField(default="default.jpg", upload_to='profile_pictures')

    def __str__(self):
        return f'{self.user.name}Profile'
    
    #resizing a larger image:
    def save(self, **kwargs):
        #super().save(self, **kwargs)->integrity error


        img=Image.open(self.image.path)

        if img.height>300 or img.width>300:
            output_size= (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    



