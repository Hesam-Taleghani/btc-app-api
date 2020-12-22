from django.urls import path, include
from rest_framework.routers import DefaultRouter
from crm import views

router = DefaultRouter()
router.register('countries', views.CountryViewSet)
app_name = 'crm'

urlpatterns = [
    path('', include(router.urls), name='countries')
]
