from django.urls import path
from .views import register_user, user_list, user_detail

urlpatterns = [
    path('register/', register_user, name='register-user'),
    path('users/', user_list, name='user-list'),
    path('users/<int:user_id>/', user_detail, name='user-detail'),
]