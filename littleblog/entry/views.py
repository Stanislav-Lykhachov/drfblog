from rest_framework import generics
from .serializers import EntryCreateSerializer, UserProfileCreateSerializer, RateUpdateSerializer
from .models import Entry
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissons import IsOwnerOrReadOnly
from rest_framework.response import Response


class UserProfileCreateView(generics.CreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileCreateSerializer


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

