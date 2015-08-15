from django.forms import widgets
from rest_framework import serializers
from .models import Profile, Comparison

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        models = Profile
        fields = ('img_url')