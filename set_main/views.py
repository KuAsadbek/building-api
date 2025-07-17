import random
from datetime import timedelta

from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .send_mes import send_sms
from .docs import load as docs
from api_mobile.utils.mixins import CustomResponseMixin
from .models import (
    ListingMod,CategoryMod,TypeSell,
    City,District,PhotoMod,
    FeaturesCat,FeaturesMod,
    RatingMod,SharesMod,ViewsMod,LikeMod,
    FavoritesMod,CustomUser,PhoneConfirmation,
    NearbyListMod,NearbyMod
)
from .serializer import (
    ListingSerializer,CategorySerializer,TypeSellSerializer,
    CitySerializer,DistrictSerializer,PhotoSerializer,
    FeaturesCatSerializer,FeaturesSerializer,
    RatingSerializer,SharesSerializer,ViewsSerializer,LikeSerializer,
    FavoritesSerializer,
    NearbySerializer,NearbyListSerializer,LoginSerializer,RegisterSerializer,
    CustomUserSerializer,CustomUserCreateSerializer,ConfirmRegisterSerializer
)

@docs.sms_doc
class SendCodeViewSet(ViewSet):
    @action(detail=False, methods=['post'], url_path='verify-code')
    def verify_code(self, request):
        phone = request.data.get("phone")
        code = request.data.get("code")
        if not phone or not code:
            return Response({"detail": "Номер телефона и код обязательны"}, status=400)
        
        try:
            conf = PhoneConfirmation.objects.get(phone=phone, code=code)
        except PhoneConfirmation.DoesNotExist:
            return Response({"detail": "Неверный код подтверждения"}, status=400)
        
        if conf.is_expired():
            return Response({"detail": "Код подтверждения истёк"}, status=400)
        
        return Response({"detail": "Код подтверждён"}, status=200)
    
    @action(detail=False, methods=['post'], url_path='send-code')
    def send_code(self, request):
        phone = request.data.get("phone")
        if not phone:
            return Response({"detail": "Номер телефона обязателен"}, status=400)
        
        existing = PhoneConfirmation.objects.filter(phone=phone).first()
        if existing and existing.created_at > timezone.now() - timedelta(minutes=1):
            return Response({"detail": "Код уже отправлен. Повторите через 1 минуту."}, status=429)
        
        code = f"{random.randint(100000, 999999)}"
        PhoneConfirmation.objects.update_or_create(phone=phone, defaults={"code": code, "created_at": timezone.now()})
        send_sms(phone, f"Код подтверждения для регистрации на сайте Building.uz: {code}:")
        return Response({"detail": "Код отправлен"}, status=200)

@docs.custom_user_doc
class CustomUserViewSet(CustomResponseMixin, ModelViewSet):
    queryset = CustomUser.objects.all()
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CustomUserCreateSerializer  # 👉 для POST, PUT, PATCH
        return CustomUserSerializer  # 👉 для GET (list, retrieve)
    http_method_names = ['get', 'put','patch','head', 'options','delete'] 

class DashboardViewSet(ViewSet):
    def list(self, request):
        user_count = CustomUser.objects.count()
        listing_count = ListingMod.objects.count()
        data = {
            'user_count': user_count,
            'listing_count': listing_count,
        }
        return Response(data)

@docs.login_doc
class AuthViewSet(CustomResponseMixin,ViewSet):
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)

            response = Response({
                'message': 'Успешный вход',
                'user': CustomUserSerializer(user).data
            }, status=status.HTTP_200_OK)

            # Устанавливаем токены в HTTP-only cookies
            response.set_cookie(
                key='access_token',
                value=str(refresh.access_token),
                httponly=True,
                secure=True,            # True если используешь HTTPS
                samesite='Lax',         # или 'Strict'
                max_age=3600            # 1 час
            )

            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=7 * 24 * 3600   # 7 дней
            )

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)

            response = Response({
                'message': 'Успешный вход',
                'user': CustomUserSerializer(user).data
            }, status=status.HTTP_200_OK)

            # Устанавливаем токены в HTTP-only cookies
            response.set_cookie(
                key='access_token',
                value=str(refresh.access_token),
                httponly=True,
                secure=True,            # True если используешь HTTPS
                samesite='Lax',         # или 'Strict'
                max_age=3600            # 1 час
            )

            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=7 * 24 * 3600   # 7 дней
            )

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        response = Response({"message": "Вы успешно вышли"}, status=status.HTTP_200_OK)

        # Удаляем cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response

@docs.nearby_doc
class NearbyViewSet(CustomResponseMixin,ModelViewSet):
    queryset = NearbyMod.objects.all()
    serializer_class = NearbySerializer

@docs.nearby_list_doc
class NearbyListViewSet(CustomResponseMixin,ModelViewSet):
    queryset = NearbyListMod.objects.all()
    serializer_class = NearbyListSerializer

@docs.features_cat_doc
class FeaturesCatViewSet(CustomResponseMixin,ModelViewSet):
    queryset = FeaturesCat.objects.all()
    serializer_class = FeaturesCatSerializer

@docs.features_doc
class FeaturesViewSet(CustomResponseMixin,ModelViewSet):
    queryset = FeaturesMod.objects.all()
    serializer_class = FeaturesSerializer

@docs.listing_doc
class ListingViewSet(CustomResponseMixin,ModelViewSet):
    queryset = ListingMod.objects.all()
    serializer_class = ListingSerializer

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['lang'] = self.request.LANGUAGE_CODE  # или см. ниже альтернативу
    #     return context
    
    #request.LANGUAGE_CODE ЕСЛИ НЕ РАБОТАЕТ
    def get_serializer_context(self):
        context = super().get_serializer_context()
        lang = self.request.headers.get('Accept-Language', 'uz')[:2].lower()
        context['lang'] = lang if lang in ['uz', 'ru', 'en'] else 'uz'
        return context

    @docs.promote_doc
    @action(detail=True, methods=['post'], url_path='promote')
    def promote(self, request, pk=None):
        listing = self.get_object()
        duration_days = int(request.data.get("days", 7))

        listing.is_promoted = True
        listing.promotion_expiry = timezone.now() + timezone.timedelta(days=duration_days)
        listing.save()

        return Response({"message": f"Объявление продвинуто на {duration_days} дней"})

@docs.category_doc
class CategoryViewSet(CustomResponseMixin,ModelViewSet):
    queryset = CategoryMod.objects.all()
    serializer_class = CategorySerializer

@docs.typesell_doc
class TypeSellViewSet(CustomResponseMixin,ModelViewSet):
    queryset = TypeSell.objects.all()
    serializer_class = TypeSellSerializer

@docs.city_doc
class CityViewSet(CustomResponseMixin,ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

@docs.district_doc
class DistrictViewSet(CustomResponseMixin,ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

@docs.photo_doc
class PhotoViewSet(CustomResponseMixin,ModelViewSet):
    queryset = PhotoMod.objects.all()
    serializer_class = PhotoSerializer

@docs.rating_doc
class RatingViewSet(CustomResponseMixin,ModelViewSet):
    queryset = RatingMod.objects.all()
    serializer_class = RatingSerializer

@docs.shares_doc
class SharesViewSet(CustomResponseMixin,ModelViewSet):
    queryset = SharesMod.objects.all()
    serializer_class = SharesSerializer

@docs.views_doc
class ViewsViewSet(CustomResponseMixin,ModelViewSet):
    queryset = ViewsMod.objects.all()
    serializer_class = ViewsSerializer

@docs.like_doc
class LikeViewSet(CustomResponseMixin,ModelViewSet):
    queryset = LikeMod.objects.all()
    serializer_class = LikeSerializer

@docs.favorites_doc
class FavoritesViewSet(CustomResponseMixin,ModelViewSet):
    queryset = FavoritesMod.objects.all()
    serializer_class = FavoritesSerializer
