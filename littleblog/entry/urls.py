from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserProfileListCreateView, EntryViewSet

app_name = 'entry'

router = DefaultRouter()
router.register('entries', EntryViewSet)

urlpatterns = [
    path('profiles/', UserProfileListCreateView.as_view()),
]

urlpatterns += router.urls

