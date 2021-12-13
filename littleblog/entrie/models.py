from django.db import models


class Author(models.Model):

    name = models.CharField(max_length=255)
    email = models.EmailField()

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

class Article(models.Model):

    title = models.CharField(max_length=130)
    text = models.TextField()
    author = models.ForeignKey('Author', related_name='articles', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title