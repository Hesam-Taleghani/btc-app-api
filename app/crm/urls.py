from django.urls import path, include
from rest_framework.routers import DefaultRouter
from crm import views

router = DefaultRouter()
router.register('countries', views.CountryViewSet)
router.register('companies', views.POSCompanyViewSet)
router.register('poses', views.PosViewSet)
router.register('services', views.ServiceViewSet)
router.register('goals', views.GoalViewSet)

app_name = 'crm'

urlpatterns = [
    path('', include(router.urls), name='countries'),
    path('company/<int:pk>/create-model/', views.POSModelCreateView.as_view(), name='create-pos-model'),
    path('posmodels/', views.POSModelListView.as_view(), name='posmodels-list'),
    path('company/<int:pk>/models/', views.PosModelCompanyList.as_view(), name='company-models'),
    path('is-used/country/<int:pk>/', views.CountryIsUsed.as_view(), name='country-used'),
    path('is-used/company/<int:pk>/', views.CompanyIsUsed.as_view(), name='company-used'),
    path('is-used/model/<int:pk>/', views.PosModelIsUsed.as_view(), name='model-used'),
    path('is-used/pos/<int:pk>/', views.POSIsUsed.as_view(), name='pos-used'),
    path('is-used/service/<int:pk>/', views.ServiceIsUsed.as_view(), name='service-used'),
    path('pos-active/<int:pk>/', views.ActivePos.as_view(), name='pos-active')
]
