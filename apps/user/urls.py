from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView, UserDetailAPIView, UserUpdateAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('me/', UserDetailAPIView.as_view(), name='user-view'),
    path('update/', UserUpdateAPIView.as_view(), name='user-update')
    # TODO: Add endpoint that fetches info about user by id
    # TODO: Add endpoint that fetches user by username
    
]
