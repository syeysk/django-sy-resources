from rest_framework import serializers


class ResourceTakeAnyToMakeSerializer(serializers.Serializer):
    fabric_id = serializers.IntegerField(help_text='Фабрика')
