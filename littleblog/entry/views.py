from rest_framework import generics
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import EntryCreateSerializer, UserProfileCreateSerializer, RatingUpdateSerializer, EntryDetailSerializer
from .models import Entry
from .permissons import IsOwnerOrReadOnly, IsAuthenticatedOrWriteOnly
from .services import set_mark


class UserProfileListCreateView(generics.ListCreateAPIView):

    serializer_class = UserProfileCreateSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticatedOrWriteOnly,)


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        entry = self.get_object()
        serializer = RatingUpdateSerializer(entry, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        set_mark(serializer.instance, **serializer.validated_data)  # rating logic storing in services.py
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'create':
            return EntryCreateSerializer
        return EntryDetailSerializer
