from django.shortcuts import render
from rest_framework import generics
from .serializers import ArticleCreateSerializer, AuthorCreateSerializer
from .models import Article


class AuthorCreateView(generics.CreateAPIView):

    serializer_class = AuthorCreateSerializer


class ArticleCreateView(generics.CreateAPIView):

    serializer_class = ArticleCreateSerializer


