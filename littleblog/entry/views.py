from django.shortcuts import render
from rest_framework import generics
from .serializers import EntryCreateSerializer, UserProfileCreateSerializer, RateUpdateSerializer
from .models import Entry, UserProfile
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class UserProfileCreateView(generics.CreateAPIView):

    #permission_classes = [IsAuthenticated]
    serializer_class = UserProfileCreateSerializer


class EntryCreateView(generics.CreateAPIView):

    serializer_class = EntryCreateSerializer


class RateUpdateView(generics.UpdateAPIView):

    serializer_class = RateUpdateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.sum_of_marks += int(request.query_params['mark'])
        instance.amount_of_marks += 1
        instance.current_rate = instance.sum_of_marks/instance.amount_of_marks
        #serializer = self.get_serializer(instance)
        #serializer.save()
        instance.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(self.serializer_class(instance).data)

    def get_queryset(self):
        return Entry.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = generics.get_object_or_404(queryset,pk=self.request.query_params['pk'])
        return obj

