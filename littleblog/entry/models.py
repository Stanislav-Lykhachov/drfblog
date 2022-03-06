from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars')

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class Entry(models.Model):

    title = models.CharField(max_length=130)
    text = models.TextField()
    author = models.ForeignKey('UserProfile', related_name='articles', on_delete=models.CASCADE)
    preview_image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    sum_of_marks = models.IntegerField(default=0)
    current_rate = models.FloatField(default=0)
    amount_of_marks = models.IntegerField(default=0)

    objects = models.Manager

    def __str__(self):
        return self.title