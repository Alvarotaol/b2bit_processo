from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('search/', PostSearchView.as_view(), name='post-search'),
]
