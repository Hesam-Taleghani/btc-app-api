from django.urls import path, include
from rest_framework.routers import DefaultRouter
from crm import views

router1 = DefaultRouter()
router1.register('countries', views.CountryViewSet)
router2 = DefaultRouter()
router2.register('companies', views.POSCompanyViewSet)
app_name = 'crm'

urlpatterns = [
    path('', include(router1.urls), name='countries'),
    path('', include(router2.urls), name='companies')
]
