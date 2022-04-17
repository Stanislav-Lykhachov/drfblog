from django.urls import path
from .views import UserProfileCreateRetrieveView, EntryViewSet, RateUpdateView
from rest_framework.routers import DefaultRouter

app_name = 'entry'

router = DefaultRouter()
router.register('entries', EntryViewSet)

urlpatterns = [
    path('profile/', UserProfileCreateRetrieveView.as_view()),
    path('profile/<int:pk>/', UserProfileCreateRetrieveView.as_view()),
    path('rate_entry/', RateUpdateView.as_view())
]

urlpatterns += router.urls

