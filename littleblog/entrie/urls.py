from django.urls import path, include
from .views import AuthorCreateView,ArticleCreateView


urlpatterns = [
    path('CreateAuthor/', AuthorCreateView.as_view()),
    path('CreateArticle/', ArticleCreateView.as_view())
    ]
