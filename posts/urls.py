from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view),
    path('posts/', views.post_list_view),
    path('posts/<int:post_id>', views.post_detail_view),
    path('createPost', views.post_create_view)
]