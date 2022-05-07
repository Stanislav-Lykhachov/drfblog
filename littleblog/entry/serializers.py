from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import Entry, UserProfile


class UserProfileCreateSerializer(serializers.ModelSerializer):

    profile = serializers.ReadOnlyField(source='profile.nickname')
    nickname = serializers.CharField(source="profile.nickname")
    avatar = serializers.ImageField(source="profile.avatar", required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'nickname', 'avatar', 'profile')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'validators': [UniqueValidator(queryset=User.objects.all())]},
            'nickname': {'validators': [UniqueValidator(queryset=User.objects.all())]}
        }

    def validate(self, attrs):
        validate_password(attrs["password"], user=User(username=attrs["username"]))
        return attrs

    def create(self, validated_data):
        credentials = {'username': validated_data.pop('username'), 'password': validated_data.pop('password')}
        user = User.objects.create_user(**credentials)
        UserProfile.objects.create(user=user, **validated_data['profile'])
        return user


class EntryCreateSerializer(serializers.ModelSerializer):

    class CurrentAuthor:

        requires_context = True

        def __call__(self, serializer_field):
            return serializer_field.context['request'].user.profile

        def __repr__(self):
            return '%s()' % self.__class__.__name__

    author = serializers.HiddenField(default=CurrentAuthor())

    class Meta:
        model = Entry
        fields = ('id', 'title', 'text', 'author', 'preview_image', 'topic',)


class EntryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = ('id', 'title', 'text', 'author', 'preview_image', 'topic',)


class RateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = '__all__'






