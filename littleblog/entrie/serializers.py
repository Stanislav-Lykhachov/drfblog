from rest_framework import serializers
from .models import Article, Author


class AuthorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class ArticleCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'
