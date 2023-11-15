from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


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


class FabricListView(APIView):
    @extend_schema(
        parameters=[
        ],
        tags=['Фабрики'],
        summary='Получить список фабрик',
    )
    def get(self, request):
        ...


class FabricCreateView(APIView):
    @extend_schema(
        parameters=[
        ],
        tags=['Фабрики'],
        summary='Добавить фабрику',
    )
    def post(self, request):
        ...


class FabricView(APIView):
    @extend_schema(
        parameters=[
            fabric_id_parameter
        ],
        tags=['Фабрики'],
        summary='Получить фабрику',
    )
    def get(self, request, fabric_id):
        ...

    @extend_schema(
        parameters=[
            fabric_id_parameter
        ],
        tags=['Фабрики'],
        summary='Изменить фабрику',
    )
    def put(self, request, fabric_id):
        ...

    @extend_schema(
        parameters=[
            fabric_id_parameter
        ],
        tags=['Фабрики'],
        summary='Удалить фабрику',
    )
    def delete(self, request, fabric_id):
        ...
