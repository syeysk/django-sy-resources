from django.urls import path, include


urlpatterns = [
    path('', include('django_sy_framework.base.urls_api')),
    path('v1/linker/', include('django_sy_framework.linker.urls_api')),
    path('v1/fabric/', include('fabric.urls_api')),
    path('v1/resource/', include('resource.urls_api')),
]
