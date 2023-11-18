from rest_framework import serializers

from fabric.models import Fabric
from resource.models import Resource


class DefaultListSerializer(serializers.Serializer):
    p = serializers.IntegerField(help_text='Номер страницы', default=1, allow_null=False, min_value=1)
    c = serializers.IntegerField(
        help_text='Количество объектов на странице',
        default=15,
        allow_null=False,
        min_value=1,
    )
    s = serializers.CharField(help_text='строка поиска', default='', allow_null=False)


class ResourceTakeAnyToMakeSerializer(serializers.Serializer):
    error_messages = {'fabric_not_exists': 'Fabric not exists'}
    fabric = serializers.IntegerField(help_text='Фабрика')

    def validate_fabric(self, value):
        fabric = Fabric.objects.filter(pk=value).first()
        if not fabric:
            self.fail('fabric_not_exists')

        return fabric


class ResourceTakeAnyToMakeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'title']


class ResourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['title', 'status', 'fabric_maker']


class ResourceCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id']


class ResourceGetResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'title', 'status', 'fabric_maker']
