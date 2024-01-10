from django.urls import path

from resource.views import (
    ResourceAddImagesView,
    ResourceDeleteImageView,
    ResourceEditView,
    ResourceListView,
    ResourceSetMainImageView,
    ResourceView,
)


urlpatterns = [
    path('show-me-list', ResourceListView.as_view(), name='resource_list'),
    path('<int:pk>', ResourceView.as_view(), name='resource'),
    path('<int:pk>/edit', ResourceEditView.as_view(), name='resource_post'),
    path('<int:pk>/images/add', ResourceAddImagesView.as_view(), name='resource_images_add'),
    path('<int:pk>/image/<int:pk_image>/delete', ResourceDeleteImageView.as_view(), name='resource_delete_image'),
    path('<int:pk>/image/<int:pk_image>/set_main', ResourceDeleteImageView.as_view(), name='resource_set_main_image'),
    path('new/edit', ResourceEditView.as_view(), name='resource_create_post'),
    path('new', ResourceView.as_view(), name='resource_create'),
]
