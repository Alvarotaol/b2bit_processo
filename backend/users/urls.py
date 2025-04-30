# users/urls.py

from django.urls import path
from .views import *


urlpatterns = [
	path('me/', MeView.as_view(), name='me'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('follow/<int:user_id>/', FollowUser.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', UnfollowUser.as_view(), name='unfollow'),
    path('profile/', ProfileView.as_view(), name='my-profile'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='user-profile'),
    path('<int:user_id>/posts/', UserPostsView.as_view(), name='user-posts'),
]