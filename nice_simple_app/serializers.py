from django.forms import widgets
from rest_framework import serializers
from .models import Profile, Comparison
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id',
                  'public_view',
                  'img_url',
                  'p_name',
                  'p_phone',
                  'p_city',
                  'p_region',
                  'p_country',
                  'p_birthday',
                  'p_birthyear',
                  'p_relationship',
                  'p_relationship_with',
                  'p_job_title',
                  'p_job_employer',
                  'p_studying',
                  'p_school',
                  'p_friends',
                  'p_likes',
                  'p_groups',
                  'p_information',
                  'p_quotes',
                  'p_nickname'
                  )

class UserSerializer(serializers.ModelSerializer):
    urls = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all())

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'urls')