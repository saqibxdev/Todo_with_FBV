
from django.urls import path
from api import views
urlpatterns = [
    path('users/',views.users_list,name='users'),
    path('users/<int:pk>/',views.users_detail,name='users'),
]
