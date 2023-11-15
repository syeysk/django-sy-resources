from django.shortcuts import get_object_or_404
from django_sy_framework.custom_auth.authentication import TokenAuthentication
from django_sy_framework.custom_auth.permissions import CheckIsUsernNotAnonymousUser
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from fabric.models import Fabric
from fabric.serializers import (
    FabricCreateSerializer,
    FabricCreateResponseSerializer,
    FabricGetResponseSerializer,
)


fabric_id_parameter = OpenApiParameter(
    name='fabric_id',
    description='Идентификатор фабрики',
    required=True,
    type=int,
    location=OpenApiParameter.PATH,
    examples=[
        OpenApiExample('пример', value='1')
    ]
)


class Auth(OpenApiAuthenticationExtension):
    name = 'Token authentication'
    target_class = TokenAuthentication

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'name': 'AUTHORIZATION',
            'in': 'header',
            'scheme': 'Bearer',
        }


class FabricListView(APIView):
    @extend_schema(
        parameters=[
        ],
        tags=['Фабрики'],
        summary='Получить список фабрик',
    )
    def get(self, request):
        """Метод отдаёт список фабрик"""


class FabricCreateView(APIView):
    """Класс с методом для добавления новой фабрики"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [CheckIsUsernNotAnonymousUser]
    # DRF_STANDARDIZED_ERRORS = {
    #     'ALLOWED_ERROR_STATUS_CODES': ["400", "403", "404", "429"]
    # }

    @extend_schema(
        request=FabricCreateSerializer,
        responses={201: FabricCreateResponseSerializer, 400: None},
        tags=['Фабрики'],
        summary='Добавить фабрику',
    )
    def post(self, request):
        """Метод добавляет новую фабрику"""
        serializer = FabricCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fabric = serializer.save(user=request.user)
        response_serializer = FabricCreateResponseSerializer(instance=fabric)
        return Response(status=status.HTTP_201_CREATED, data=response_serializer.data)


class FabricView(APIView):
    """Класс методов для работы с фабрикой"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [CheckIsUsernNotAnonymousUser]

    @extend_schema(
        parameters=[
            fabric_id_parameter
        ],
        responses={200: FabricGetResponseSerializer, 404: None},
        tags=['Фабрики'],
        summary='Получить фабрику',
    )
    def get(self, _, fabric_id):
        """Метод возвращает существующую фабрику"""
        fabric = get_object_or_404(Fabric, pk=fabric_id)
        response_serializer = FabricGetResponseSerializer(instance=fabric)
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)

    @extend_schema(
        parameters=[
            fabric_id_parameter
        ],
        tags=['Фабрики'],
        summary='Изменить фабрику',
    )
    def put(self, request, fabric_id):
        """Метод изменяет существующую фабрику"""

    @extend_schema(
        parameters=[
            fabric_id_parameter
        ],
        tags=['Фабрики'],
        summary='Удалить фабрику',
    )
    def delete(self, request, fabric_id):
        """Метод удаляет существующую фабрику"""
