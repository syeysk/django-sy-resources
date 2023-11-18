from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from resource.models import Resource
from resource.serializers_api import (
    DefaultListSerializer,
)
from resource.serializers import (
    ResourceCreateSerializer,
    ResourceUpdateSerializer,
)


class ResourceListView(View):
    def get(self, request):
        serializer = DefaultListSerializer(data=request.GET)
        serializer.is_valid()
        params = serializer.validated_data

        resource_queryset = Resource.objects.all().order_by('-pk')
        paginator = Paginator(resource_queryset, params.get('c', 15))
        page = paginator.page(params.get('p', 1))
        resources = []
        statuses = dict(Resource.STATUS_CHOICES)
        for resource in page.object_list:
            status = statuses[resource.status]
            resources.append(
                {'pk': resource.pk, 'title': resource.title, 'status': status, 'fabric_maker': resource.fabric_maker},
            )

        context = {'resources': resources}
        return render(request, 'resource/resource_list.html', context)


class ResourceView(View):
    def get(self, request, pk=None):
        """Метод отдаёт ресурс"""
        statuses = dict(Resource.STATUS_CHOICES)
        if not pk:
            if not request.user.is_authenticated:
                return redirect(settings.LOGIN_URL)

            context = {'resource': None, 'statuses': statuses, 'has_access_to_edit': True}
            return render(request, 'resource/resource.html', context)

        resource = get_object_or_404(Resource, pk=pk)
        context = {
            'resource': {
                'pk': resource.pk,
                'title': resource.title,
                'status': resource.status,
            },
            'statuses': statuses,
            'has_access_to_edit': request.user.is_authenticated and resource.user_adder == request.user,
        }
        return render(request, 'resource/resource.html', context)


class ResourceEditView(APIView):
    def post(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        response_data = {}
        if pk:
            resource = get_object_or_404(Resource, pk=pk)
            if request.user.pk != resource.user_adder.pk:
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer = ResourceUpdateSerializer(resource, data=request.data)
            serializer.is_valid(raise_exception=True)
            response_data['updated_fields'] = [
                name for name, value in serializer.validated_data.items() if getattr(resource, name) != value
            ]
            serializer.save()
        else:
            serializer = ResourceCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            resource = serializer.create({**serializer.validated_data, 'user_adder': request.user})
            response_data['pk'] = resource.pk

        return Response(status=status.HTTP_200_OK, data=response_data)
