from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import (
    ListingMobViewSet
)

app_name = 'api_mobile'

router = DefaultRouter()

router.register(r'listing-mob',ListingMobViewSet,basename='listing-mob')

urlpatterns = [
    path('v2/',include(router.urls)),
]
