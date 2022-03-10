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
        Сделаем так, чтобы User и UserProfile создавались одним махом, но оно не сработало.... Получил в своём browsable API
        Вот такое    ""detail": "JSON parse error - Expecting ',' delimiter: line 5 column 5 (char 76)""
        """
        #request_dict = json.load(request.data)
        #credentials = {'username': request_dict.pop('username'), 'password': request_dict.pop('password')}
        #usermodel = get_user_model()
        #created_user = usermodel.objects.create_user(*credentials)
        #request_dict['user'] = created_user.id
        #json.dump(request_dict)
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

