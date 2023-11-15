from rest_framework import serializers

from fabric.models import Fabric


class FabricCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabric
        fields = ['title']


class FabricCreateResponseSerializer(serializers.ModelSerializer):
    """Успешно добавленная фабрика"""
    class Meta:
        model = Fabric
        fields = ['id']


class FabricGetResponseSerializer(serializers.ModelSerializer):
    """Фабрика"""
    class Meta:
        model = Fabric
        fields = ['id', 'title']
