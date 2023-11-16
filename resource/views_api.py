from django.shortcuts import get_object_or_404
from django_sy_framework.custom_auth.authentication import TokenAuthentication
from django_sy_framework.custom_auth.permissions import CheckIsUsernNotAnonymousUser
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from resource.models import Resource
from resource.serializers import (
    ResourceTakeAnyToMakeSerializer,
    ResourceCreateSerializer,
    ResourceCreateResponseSerializer,
    ResourceGetResponseSerializer,
    ResourceTakeAnyToMakeResponseSerializer,
)


resource_id_parameter = OpenApiParameter(
    name='resource_id',
    description='Идентификатор ресурса',
    required=True,
    type=int,
    location=OpenApiParameter.PATH,
    examples=[
        OpenApiExample('пример', value='1')
    ]
)


class ResourceListView(APIView):
    @extend_schema(
        parameters=[
        ],
        tags=['Ресурсы'],
        summary='Получить список ресурсов',
    )
    def get(self, request):
        """Метод отдаёт список ресурсов"""


class ResourceCreateView(APIView):
    """Класс с методом для добавления ресурса"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [CheckIsUsernNotAnonymousUser]

    @extend_schema(
        parameters=[
        ],
        request=ResourceCreateSerializer,
        responses={201: ResourceCreateResponseSerializer, 400: None},
        tags=['Ресурсы'],
        summary='Добавить ресурс',
    )
    def post(self, request):
        """Метод добавляет новый ресурс"""
        serializer = ResourceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user_adder=request.user)
        response_serializer = ResourceCreateResponseSerializer(instance=instance)
        return Response(status=status.HTTP_201_CREATED, data=response_serializer.data)


class ResourceView(APIView):
    """Класс методов для работы с ресурсом"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [CheckIsUsernNotAnonymousUser]

    @extend_schema(
        parameters=[
            resource_id_parameter,
        ],
        responses={200: ResourceGetResponseSerializer, 404: None},
        tags=['Ресурсы'],
        summary='Получить ресурс',
    )
    def get(self, _, resource_id):
        """Метод отдаёт ресурс"""
        resource = get_object_or_404(Resource, pk=resource_id)
        response_serializer = ResourceGetResponseSerializer(instance=resource)
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)

    @extend_schema(
        parameters=[
            resource_id_parameter
        ],
        responses={},
        tags=['Ресурсы'],
        summary='Изменить ресурс',
    )
    def put(self, request, resource_id):
        """Метод изменяет существующий ресурс"""

    @extend_schema(
        parameters=[
            resource_id_parameter
        ],
        responses={},
        tags=['Ресурсы'],
        summary='Удалить ресурс',
    )
    def delete(self, request, resource_id):
        """Метод удаляет существующий новый ресурс"""


class ResourceTakeAnyToMakeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CheckIsUsernNotAnonymousUser]

    @extend_schema(
        parameters=[
        ],
        request=ResourceTakeAnyToMakeSerializer,
        responses={200: ResourceTakeAnyToMakeResponseSerializer, 204: None, 400: None},
        tags=['Ресурсы'],
        summary='Получить первый в очереди ресурс на изготовление',
    )
    def put(self, request):
        """Метод отдаёт первый в очереди ресурс для изготовления, предварительно отметив его как "В процессе" """
        serializer = ResourceTakeAnyToMakeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        resource_to_make = Resource.objects.filter(status=Resource.STATUS_CHOICE_REQUIRED).first()
        if not resource_to_make:
            return Response(status=status.HTTP_204_NO_CONTENT)

        resource_to_make.fabric_maker = data['fabric']
        resource_to_make.status = Resource.STATUS_CHOICE_IN_MAKING
        resource_to_make.save()

        response_serializer = ResourceTakeAnyToMakeResponseSerializer(instance=resource_to_make)
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)
