from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from resource.models import Resource
from resource.serializers import (
    DefaultListSerializer,
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
    def get(self, request, resource_id=None):
        """Метод отдаёт ресурс"""
        statuses = dict(Resource.STATUS_CHOICES)
        if not resource_id:
            if not request.user.is_authenticated:
                return redirect(settings.LOGIN_URL)

            context = {'resource': None, 'statuses': statuses, 'has_access_to_edit': True}
            return render(request, 'resource/resource.html', context)

        resource = get_object_or_404(Resource, pk=resource_id)
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
