from rest_framework import generics
from rest_framework import viewsets
from .serializers import EntryCreateSerializer, UserProfileCreateSerializer, RateUpdateSerializer, EntryDetailSerializer
from .models import Entry
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .permissons import IsOwnerOrReadOnly, IsAuthenticatedOrWriteOnly
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status


class UserProfileListCreateView(generics.ListCreateAPIView):

    serializer_class = UserProfileCreateSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticatedOrWriteOnly,)


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return EntryCreateSerializer
        return EntryDetailSerializer


class RateUpdateView(generics.UpdateAPIView):
    """
    Вот это есть та самая вьюшка, которая отвечает за подсчет рейтинга записи.
    В url нужно дописать в виде параметров pk и mark (оценка, которую ставишь) и отправить PATCH request
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = RateUpdateSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.sum_of_marks += int(request.query_params['mark'])
        instance.amount_of_marks += 1
        instance.current_rate = instance.sum_of_marks / instance.amount_of_marks
        instance.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(self.serializer_class(instance).data)

    def get_queryset(self):
        return Entry.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = generics.get_object_or_404(queryset, pk=self.request.query_params['pk'])
        return obj
