from rest_framework import generics
from rest_framework import viewsets
from .serializers import EntryCreateSerializer, UserProfileCreateSerializer, RateUpdateSerializer, EntryDetailSerializer
from .models import Entry
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .permissons import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status


class UserProfileCreateView(generics.CreateAPIView):

    serializer_class = UserProfileCreateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.dict()
        data.pop('username')
        data.pop('password')
        data['user'] = kwargs.pop('user')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        """
        Сделаем так, чтобы User и UserProfile создавались одним махом. УРА! В этом коммите я сделал это! Для минимального
        POST запроса нужны :  username и password (для создания модельки User), и nickname для модельки UserProfile.
        """
        usermodel = get_user_model()
        user = usermodel.objects.create_user(username=request.data['username'], password=request.data['password'])
        kwargs['user'] = user.pk

        return self.create(request, *args, **kwargs)


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

