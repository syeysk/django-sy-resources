from rest_framework import serializers

from fabric.models import Fabric


class ResourceTakeAnyToMakeSerializer(serializers.Serializer):
    error_messages = {'fabric_not_exists': 'Fabric not exists'}
    fabric = serializers.IntegerField(help_text='Фабрика')

    def validate_fabric(self, value):
        fabric = Fabric.objects.filter(pk=value).first()
        if not fabric:
            self.fail('fabric_not_exists')

        return fabric
