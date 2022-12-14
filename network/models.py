from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    pass
    def __str__(self):
        return self.username

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000, validators=[MinLengthValidator(1)])
    creation = models.DateTimeField(default=timezone.now())
    likes = models.IntegerField(default=0)
    def __str__(self):
        return f"By {self.owner} at {self.creation}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='followers')
    def __str__(self):
        return f"{self.user} followed by {self.followers.count()}"