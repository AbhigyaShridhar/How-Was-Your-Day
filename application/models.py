from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Theme(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name

class Room(models.Model):
    people = models.ManyToManyField(User, null=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, null=True)
    full = models.BooleanField(default=False)

class BinaryRoom(models.Model):
    person1 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="person1_in_room")
    person2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="person2_in_room")

class Message(models.Model):
    text = models.TextField();
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    binary_room = models.ForeignKey(BinaryRoom, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Clip(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    audio = models.FileField(upload_to='audio/')

    class Meta:
        db_table = 'Audio_store'
