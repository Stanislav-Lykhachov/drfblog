from rest_framework import serializers
from .models import Entry, UserProfile
from django.contrib.auth.models import User


class UserProfileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'


class EntryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        exclude = ['sum_of_marks', 'current_rate', 'amount_of_marks']


class RateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = '__all__'






