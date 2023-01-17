from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    pass
    def __str__(self):
        return self.username

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500, validators=[MinLengthValidator(1)])
    creation = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    def __str__(self):
        return f"By {self.owner} at {self.creation}"
    def serialize(self):
        return {
            "id": self.pk,
            "owner": self.owner.username,
            "content": self.content,
            "creation": self.creation,
            "likes": self.likes
        }

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    def __str__(self):
        return f"{self.follower} is following {self.user}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user} likes {self.post}"