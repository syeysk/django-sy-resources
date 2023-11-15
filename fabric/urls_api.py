from django.urls import path

from fabric.views_api import FabricView, FabricCreateView, FabricListView


urlpatterns = [
    path('<int:fabric_id>', FabricView.as_view(), name='fabric'),
    path('new', FabricCreateView.as_view(), name='fabric_create'),
    path('', FabricListView.as_view(), name='fabric_list'),
]
