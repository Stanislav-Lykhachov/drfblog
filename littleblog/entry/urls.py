from django.urls import path, include
from .views import UserProfileCreateView,EntryCreateView, RateUpdateView


urlpatterns = [
    path('CreateUserProfile/', UserProfileCreateView.as_view()),
    path('CreateEntry/', EntryCreateView.as_view()),
    path('set_mark/', RateUpdateView.as_view())
    ]
