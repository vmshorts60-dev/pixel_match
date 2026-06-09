from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_image = models.ImageField(upload_to='profiles/',blank=True,
    null=True )
    age = models.IntegerField()
    gender = models.CharField(max_length=20)

    bio = models.TextField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Match(models.Model):
    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user1_matches'
    )

    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user2_matches'
    )

    matched_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{self.user1.username} ❤️ {self.user2.username}"


class Like(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes_sent'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes_received'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{self.sender.username} liked {self.receiver.username}"


class ProfilePhoto(models.Model):
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='photos'
    )

    image = models.ImageField(
        upload_to='profile_photos/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.profile.user.username} Photo"



class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages"
    )

    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_seen = models.BooleanField(default=False)

