from rest_framework import serializers

from resource.models import Resource, ImageResource, ModelResource


class ResourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['title', 'status']


class ResourceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['title', 'status']
        extra_kwargs = {
            'title': {'required': False},
            'status': {'required': False},
        }


class ResourceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageResource
        fields = ['pk', 'is_main', 'image']


class ResourceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelResource
        fields = ['pk', 'model_type']
