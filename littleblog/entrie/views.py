from django.shortcuts import render
from rest_framework import generics
from .serializers import ArticleCreateSerializer
from .models import Article

class ArticleCreateView(generics.CreateAPIView):
    serializer_class = ArticleCreateSerializer
