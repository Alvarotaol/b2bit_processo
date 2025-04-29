# users/urls.py

from django.urls import path
from .views import SignupView, LoginView, LogoutView, TokenRefreshView, FollowUser, UnfollowUser, MeView


urlpatterns = [
	path('me/', MeView.as_view(), name='me'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('follow/<int:user_id>/', FollowUser.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', UnfollowUser.as_view(), name='unfollow'),
]