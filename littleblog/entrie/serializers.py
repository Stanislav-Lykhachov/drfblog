from rest_framework import serializers
from .models import Article

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (__all__)
