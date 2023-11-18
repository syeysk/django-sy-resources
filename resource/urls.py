from django.urls import path

from resource.views import (
    ResourceListView,
    ResourceView,
)


urlpatterns = [
    path('show-me-list', ResourceListView.as_view(), name='resource_list'),
    path('<int:resource_id>', ResourceView.as_view(), name='resource'),
    path('new', ResourceView.as_view(), name='resource_create'),
]
