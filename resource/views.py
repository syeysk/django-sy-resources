import os

from django.conf import settings
from django.core.files.images import ImageFile
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django_sy_framework.utils.utils import make_file_hash

from resource.models import Resource, ImageResource, ModelResource
from resource.serializers_api import (
    DefaultListSerializer,
)
from resource.serializers import (
    ResourceCreateSerializer,
    ResourceImageSerializer,
    ResourceModelSerializer,
    ResourceUpdateSerializer,
)
from utils.constants import (
    BEFORE_CREATE,
    BEFORE_OPEN_CREATE_PAGE,
    BEFORE_OPEN_VIEW_PAGE,
    BEFORE_UPDATE,
    CREATED,
    UPDATED,
    WEB,
)
from utils.hooks import resource_hook
from utils.hook_meta import CreatedResource, CreatePageNote, ViewPageNote, UpdatedNote


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
            main_image = resource.images.order_by('-is_main').first()
            resource_status = statuses[resource.status]
            resources.append(
                {
                    'pk': resource.pk,
                    'title': resource.title,
                    'status': resource_status,
                    'fabric_maker': resource.fabric_maker,
                    'main_image': ResourceImageSerializer(instance=main_image).data if main_image else None,
                },
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
        image_serializer = ResourceImageSerializer(instance=resource.images.order_by('-is_main'), many=True)
        model_serializer = ResourceModelSerializer(instance=resource.models.defer('model'), many=True)
        context = {
            'resource': {
                'pk': resource.pk,
                'title': resource.title,
                'status': resource.status,
                'images': image_serializer.data,
                'models': model_serializer.data,
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
            data = serializer.validated_data

            meta = CreatedResource(data['title'], data['status'], None, request)
            resource_hook(BEFORE_CREATE, WEB, meta)
            if meta.errors:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=meta.errors)

            meta.created_resource = serializer.create({**data, 'user_adder': request.user})
            resource_hook(CREATED, WEB, meta)
            response_data['pk'] = meta.created_resource.pk

        return Response(status=status.HTTP_200_OK, data=response_data)


class ResourceAddImagesView(APIView):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        resource = get_object_or_404(Resource, pk=pk)
        if request.user.pk != resource.user_adder.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serialized_valid_images = []
        for uploaded_image in request.FILES.getlist('images'):
            file_hash = make_file_hash(uploaded_image)
            _, ext = os.path.splitext(uploaded_image.name)
            image_name = f'{file_hash}{ext.lower()}'
            if not os.path.exists(f'{settings.MEDIA_ROOT}/{ImageResource.UPLOAD_TO}/{image_name}'):
                image = resource.images.create(image=ImageFile(uploaded_image, image_name))
                serialized_valid_images.append(ResourceImageSerializer(instance=image).data)

        response_data = {
            'saved_images': serialized_valid_images,
            'updated_fields': ['images'] if serialized_valid_images else [],
        }
        return Response(status=status.HTTP_200_OK, data=response_data)


class ResourceDeleteImageView(APIView):
    def post(self, request, pk, pk_image):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        resource = get_object_or_404(Resource, pk=pk)
        if request.user.pk != resource.user_adder.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)

        image = get_object_or_404(ImageResource, pk=pk_image, resource=resource)
        image.delete()
        return Response(status=status.HTTP_200_OK)


class ResourceSetMainImageView(APIView):
    def post(self, request, pk, pk_image):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        resource = get_object_or_404(Resource, pk=pk)
        if request.user.pk != resource.user_adder.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)

        image = get_object_or_404(ImageResource, pk=pk_image, resource=resource)

        main_image = resource.images.filter(is_main=True).first()
        if main_image:
            main_image.is_main = False
            main_image.save()

        image.is_main = True
        image.save()
        return Response(status=status.HTTP_200_OK)
