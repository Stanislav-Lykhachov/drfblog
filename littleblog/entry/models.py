from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars', blank=True)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Topic(models.Model):
    """
    Topic table for my blog entries with many-to-many relationship
    """
    title = models.CharField(max_length=100, db_index=True, unique=True)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class Entry(models.Model):
    """
    Entry model for my blog
    """
    title = models.CharField(max_length=130, unique=True)
    text = models.TextField()
    author = models.ForeignKey(UserProfile, related_name='entries', on_delete=models.CASCADE)
    preview_image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True)
    topic = models.ManyToManyField(Topic, related_name='entries')
    sum_of_marks = models.IntegerField(default=0)
    current_rate = models.FloatField(default=0)
    amount_of_marks = models.IntegerField(default=0)

    objects = models.Manager  # Не знаю почему, но мне пришлось это явно указать, спасибо stackoverflow

    def __str__(self):
        return self.title



