from django.shortcuts import render
from rest_framework import generics
from .serializers import ArticleCreateSerializer, AuthorCreateSerializer
from .models import Article
from rest_framework.mixins import RetrieveModelMixin


class AuthorCreateView(generics.CreateAPIView):

    serializer_class = AuthorCreateSerializer


class ArticleCreateView(generics.CreateAPIView):

    serializer_class = ArticleCreateSerializer
