from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# For all Posts
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted") 
    body = models.CharField(max_length=1024)
    posted_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.id}. {self.user} posted {self.body} at {self.posted_at} & liked by {self.likes}"

    def serialize(self):
        return {
                "id": self.id,
                "user": self.user.username,
                "body": self.body,
                "time": self.posted_at,
                "likes": self.likes
                }

    class Meta:
        ordering = ["-posted_at"]


# For likes
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} liked {self.post}"


# does this need serialization

# For followers & following
class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user") 

    def __str__(self):
        return f"{self.follower} follows {self.user}"

    def serialize(self):
        return {
                "follower": self.follower.username,
                "user": self.user.username
                }


