from django.urls import path

from resource.views_api import ResourceView, ResourceCreateView, ResourceListView, ResourceTakeAnyToMakeView

urlpatterns = [
    path('<int:resource_id>', ResourceView.as_view(), name='resource'),
    path('new', ResourceCreateView.as_view(), name='resource_create'),
    path('take_any_to_make', ResourceTakeAnyToMakeView.as_view(), name='resource_take_any_to_make'),
    path('', ResourceListView.as_view(), name='resource_list'),
]
