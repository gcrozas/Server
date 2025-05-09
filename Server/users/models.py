from django.db import models

from django.contrib.auth.models import User
from PIL import Image

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics')

    class Meta:
        verbose_name = ("Perfil reistrado")
        verbose_name_plural = ("Perfiles registrados")
        ordering = ['user']

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args,**kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)