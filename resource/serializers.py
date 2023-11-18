from rest_framework import serializers

from resource.models import Resource


class ResourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['title']


class ResourceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['title', 'status']
        extra_kwargs = {
            'title': {'required': False},
            'status': {'required': False},
        }
