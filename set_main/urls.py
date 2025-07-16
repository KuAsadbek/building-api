from django.urls import path,include
from .router_set import CustomRouter
from .views import (
    ListingViewSet,CategoryViewSet,TypeSellViewSet,
    CityViewSet,DistrictViewSet,PhotoViewSet,
    FeaturesCatViewSet,FeaturesViewSet,
    RatingViewSet,SharesViewSet,ViewsViewSet,LikeViewSet,
    FavoritesViewSet,CommentViewSet,AuthViewSet,
    NearbyViewSet,NearbyListViewSet,DashboardViewSet,CustomUserViewSet,
    SendCodeViewSet
)

app_name = 'set_main'

router = CustomRouter()

router.register(r'users',CustomUserViewSet,basename='users')
router.register(r'send_sms', SendCodeViewSet, basename='send_sms')
router.register(r'listing',ListingViewSet,basename='listing')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'listing-nearby',NearbyViewSet,basename='listing-nearby')
router.register(r'listing-nearby-list',NearbyListViewSet,basename='listing-nearby-list')
router.register(r'listing-features',FeaturesViewSet,basename='listing-features')
router.register(r'features',FeaturesCatViewSet,basename='features')
router.register(r'category',CategoryViewSet,basename='category')
router.register(r'typesell',TypeSellViewSet,basename='typesell')
router.register(r'city',CityViewSet,basename='city')
router.register(r'district',DistrictViewSet,basename='district')
router.register(r'photo',PhotoViewSet,basename='photo')
router.register(r'rating',RatingViewSet,basename='rating')
router.register(r'shares',SharesViewSet,basename='shares')
router.register(r'views',ViewsViewSet,basename='views')
router.register(r'like',LikeViewSet,basename='like')
router.register(r'favorites',FavoritesViewSet,basename='favorites')
router.register(r'comment',CommentViewSet,basename='comment')
router.register(r'auth',AuthViewSet,basename='auth')

urlpatterns = [
    path('v1/',include(router.urls)),
]
