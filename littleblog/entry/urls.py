from django.urls import path, include
from .views import UserProfileCreateView, EntryDetailView, RateUpdateView


urlpatterns = [
    path('CreateUserProfile/', UserProfileCreateView.as_view()),
    path('EntryDetail/<int:pk>/', EntryDetailView.as_view()),
    path('set_mark/', RateUpdateView.as_view())
    ]
