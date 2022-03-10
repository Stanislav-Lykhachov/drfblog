from rest_framework import generics
from .serializers import EntryCreateSerializer, UserProfileCreateSerializer, RateUpdateSerializer
from .models import Entry
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissons import IsOwnerOrReadOnly
from rest_framework.response import Response
import json
from django.contrib.auth import get_user_model


class UserProfileCreateView(generics.CreateAPIView):

    serializer_class = UserProfileCreateSerializer

    def post(self, request, *args, **kwargs):
        """
        Сделаем так, чтобы User и UserProfile создавались одним махом, но оно не сработало.... Не могу понять, как передать
        сериализатору id моего created_user...request.data пробовал менять - не получается...
        """


        usermodel = get_user_model()
        created_user = usermodel.objects.create_user(username=request.data['username'], password=request.data['password'])
        return self.create(request, *args, **kwargs)


class EntryDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = EntryCreateSerializer
    queryset = Entry.objects.all()


class RateUpdateView(generics.UpdateAPIView):

    """
    Вот это есть та самая вьюшка, которая отвечает за подсчет рейтинга записи.
    В url нужно дописать в виде параметров pk и mark (оценка, которую ставишь)
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = RateUpdateSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.sum_of_marks += int(request.query_params['mark'])
        instance.amount_of_marks += 1
        instance.current_rate = instance.sum_of_marks/instance.amount_of_marks
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

