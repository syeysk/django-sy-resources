from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django_sy_framework.token.views import AllowAnyMixin, LoginRequiredMixin
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from resource.models import Resource
from resource.serializers import (
    ResourceTakeAnyToMakeSerializer,
    ResourceCreateSerializer,
    ResourceCreateResponseSerializer,
    DefaultListSerializer,
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


class ResourceListView(AllowAnyMixin, APIView):
    @extend_schema(
        parameters=[
            DefaultListSerializer
        ],
        tags=['Ресурсы'],
        summary='Получить список ресурсов',
    )
    def get(self, request):
        """Метод отдаёт список ресурсов"""
        serializer = DefaultListSerializer(data=request.GET)
        serializer.is_valid()
        params = serializer.validated_data

        resource_queryset = Resource.objects.all()
        paginator = Paginator(resource_queryset, params.get('c', 15))
        page = paginator.page(params.get('p', 1))
        response_data = []
        for resource in page.object_list:
            response_data.append({'pk': resource.pk, 'title': resource.title})

        return Response(status=status.HTTP_200_OK, data=response_data)


class ResourceCreateView(LoginRequiredMixin, APIView):
    """Класс с методом для добавления ресурса"""

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


class ResourceView(LoginRequiredMixin, APIView):
    """Класс методов для работы с ресурсом"""

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


class ResourceTakeAnyToMakeView(LoginRequiredMixin, APIView):
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
        fabric = data['fabric']
        if fabric.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'detail': 'You have no access to this fabric'})

        resource_to_make = Resource.objects.filter(status=Resource.STATUS_CHOICE_REQUIRED).first()
        if not resource_to_make:
            return Response(status=status.HTTP_204_NO_CONTENT)

        resource_to_make.fabric_maker = fabric
        resource_to_make.status = Resource.STATUS_CHOICE_IN_MAKING
        resource_to_make.save()

        response_serializer = ResourceTakeAnyToMakeResponseSerializer(instance=resource_to_make)
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)
