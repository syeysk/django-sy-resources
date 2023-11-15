from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from resource.serializers import ResourceTakeAnyToMakeSerializer


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
        ...


class ResourceCreateView(APIView):
    @extend_schema(
        parameters=[
        ],
        responses={},
        tags=['Ресурсы'],
        summary='Добавить ресурс',
    )
    def post(self, request):
        ...


class ResourceView(APIView):
    @extend_schema(
        parameters=[
            resource_id_parameter,
        ],
        responses={},
        tags=['Ресурсы'],
        summary='Получить ресурс',
    )
    def get(self, request, resource_id):
        ...

    @extend_schema(
        parameters=[
            resource_id_parameter
        ],
        responses={},
        tags=['Ресурсы'],
        summary='Изменить ресурс',
    )
    def put(self, request, resource_id):
        ...

    @extend_schema(
        parameters=[
            resource_id_parameter
        ],
        responses={},
        tags=['Ресурсы'],
        summary='Удалить ресурс',
    )
    def delete(self, request, resource_id):
        ...


class ResourceTakeAnyToMakeView(APIView):
    @extend_schema(
        parameters=[
        ],
        request=ResourceTakeAnyToMakeSerializer,
        tags=['Ресурсы'],
        summary='Получить первый в очереди ресурс на изготовление',
    )
    def put(self, request):
        ...
