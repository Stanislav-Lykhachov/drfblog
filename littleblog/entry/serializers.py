from rest_framework import serializers
from .models import Entry, UserProfile
from django.contrib.auth.models import User


class UserProfileCreateSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserProfile
        fields = '__all__'


class EntryCreateSerializer(serializers.ModelSerializer):

    class CurrentAuthor:
        """Взял я такой, значит класс serializers.CurrentUserDefault и переделал под возвращение
        инстанса UserProfile, связанного с залогиненным User, вроде ошибки не выбивает, но заносит в поле author_id
        какую-то рандомную шляпу..."""
        requires_context = True

        def __call__(self, serializer_field):
            return serializer_field.context['request'].user.profile

        def __repr__(self):
            return '%s()' % self.__class__.__name__

    author = serializers.HiddenField(default=CurrentAuthor())

    class Meta:
        model = Entry
        exclude = ['sum_of_marks', 'current_rate', 'amount_of_marks']


class EntryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        exclude = ['sum_of_marks', 'current_rate', 'amount_of_marks']


class RateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = '__all__'






