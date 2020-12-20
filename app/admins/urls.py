from django.urls import path
from admins import views

app_name = 'admins'

urlpatterns = [
    path('create/', views.CreateAdminView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
