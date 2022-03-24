from django.conf.urls.static import static
from django.urls import path, include
from .views import UserProfileCreateView, EntryDetailView, RateUpdateView, EntryCreateView

urlpatterns = [
    path('create_profile/', UserProfileCreateView.as_view()),
    path('entries/<int:pk>/', EntryDetailView.as_view()),
    path('entries/create/', EntryCreateView.as_view()),
    path('entries/<int:pk>/rate/', RateUpdateView.as_view())
    ]

