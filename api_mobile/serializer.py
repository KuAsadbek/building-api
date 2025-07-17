from rest_framework import serializers
from set_main.models import (
    ListingMod, CategoryMod, TypeSell,FeaturesCat,
    FeaturesMod, City, District, PhotoMod, RatingMod, 
    SharesMod, ViewsMod, LikeMod, FavoritesMod, 
    NearbyListMod,NearbyMod,CurrencyRate
)
from datetime import date
from decimal import Decimal
from django.contrib.auth.models import User

class PhotoMobSerializer(serializers.ModelSerializer):
    listing_name = serializers.SerializerMethodField()
    class Meta:
        model = PhotoMod
        fields = '__all__'

    def get_listing_name(self,obj) -> str:
        return obj.listing.title

class ListingMobSerializer(serializers.ModelSerializer):
    specs = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    nearby_list = serializers.SerializerMethodField()
    coordinates = serializers.SerializerMethodField()

    category = serializers.SerializerMethodField()
    types_name = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    rating_count = serializers.SerializerMethodField()
    share_count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    favorite_count = serializers.SerializerMethodField()

    class Meta:
        model = ListingMod
        fields = [
            'id', 'user', 'user_name', 'title', 'description',
            'category', 'price', 'transaction_type', 'specs', 'features',
            'mortgage_available', 'nearby_list', 'coordinates', 'status',
            'photos', 'location', 'video',
            'city', 'city_name', 'types', 'types_name',
            'like_count', 'view_count', 'share_count',
            'rating_count', 'favorite_count',
            'created_at',
        ]

    def get_language(self):
        # Пример: получаем язык из контекста запроса
        return self.context.get('lang', 'uz')

    def get_price(self, obj) -> dict:
        lang = self.get_language()  # 'uz', 'ru', 'en'

        # Определим в какую валюту нужно конвертировать
        target_currency = {
            'uz': 'UZS',
            'ru': 'RUB',
            'en': 'USD'
        }.get(lang, 'UZS')

        # Получаем курс нужной валюты на сегодня
        today = date.today()
        try:
            target_rate = CurrencyRate.objects.get(currency=target_currency, date=today).rate
        except CurrencyRate.DoesNotExist:
            target_rate = Decimal(1)  # Fallback

        try:
            base_rate = obj.currency.rate if obj.currency else Decimal(1)
        except:
            base_rate = Decimal(1)

        # Конвертация
        if base_rate == 0:
            converted_price = Decimal(0)
        else:
            converted_price = (obj.price / base_rate) * Decimal(target_rate)

        return {
            'currency': target_currency,
            'amount': round(converted_price, 2)
        }
        
    def get_language(self):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return getattr(request.user, 'language', 'uz')
        return 'uz'


    def get_fields(self):
        """Ограничиваем поля в зависимости от действия во ViewSet."""
        fields = super().get_fields()
        view = self.context.get('view', None)

        # По умолчанию — все поля
        allowed = set(self.Meta.fields)

        if view and hasattr(view, 'action'):
            if view.action == 'list':
                # Ограничим список полей для списка
                allowed = {
                    'id', 'title', 'user_name', 'price', 'specs',
                    'photos','coordinates', 'city_name', 'types_name',
                    'like_count', 'view_count', 'share_count'
                }
            elif view.action == 'retrieve':
                # Для detail оставим все поля
                allowed = set(self.Meta.fields)

        return {name: field for name, field in fields.items() if name in allowed}

    # ⬇ Все твои методы оставляем как есть:

    def get_specs(self,obj) -> dict:
        return {
            'area': obj.area,
            'age': obj.age,
            'rooms': obj.rooms,
            'floor': obj.floor,
            'bathrooms': obj.bathrooms,
            'toilets': obj.toilets,
            'furnished': obj.furnished,
            'parking': obj.parking
        }

    def get_coordinates(self, obj) -> dict:
        return {
            'lat': obj.latitude,
            'lng': obj.longitude
        }

    def get_location(self, obj) -> dict:
        return {
            'city_id': obj.district.city.id,
            'city_name': obj.district.city.name,
            'district_id': obj.district.id,
            'district': obj.district.name,
        }

    def get_nearby_list(self, obj) -> list:
        return list(obj.nearbylistmod_set.values_list('nearby__name', flat=True))

    def get_features(self, obj) -> list:
        lang = self.get_language()
        features = obj.featuresmod_set.select_related('features').all()
        return [
            {
                'id': feature.features.id,
                'name': {
                    'uz': feature.features.title_uz,
                    'en': feature.features.title_en,
                    'ru': feature.features.title_ru
                }.get(lang, feature.features.title_uz)
            }
            for feature in features
        ]

    def get_category(self, obj) -> dict:
        lang = self.get_language()
        name = {
            'uz': obj.category.name_uz,
            'en': obj.category.name_en,
            'ru': obj.category.name_ru
        }
        return {
            'id': obj.category.id,
            'name': name.get(lang, obj.category.name_uz)
        }

    def get_rating_count(self, obj) -> int:
        return obj.ratingmod_set.count()

    def get_share_count(self, obj) -> int:
        return obj.sharesmod_set.count()

    def get_view_count(self, obj) -> int:
        return obj.viewsmod_set.count()

    def get_like_count(self, obj) -> int:
        return obj.likemod_set.count()

    def get_favorite_count(self, obj) -> int:
        return obj.favoritesmod_set.count()

    def get_types_name(self, obj) -> str:
        return obj.types.name

    def get_city_name(self, obj) -> str:
        return obj.city.name

    def get_user_name(self, obj) -> str:
        return obj.user.name

    def get_photos(self, obj) -> list:
        return PhotoMobSerializer(obj.photomod_set.all(), many=True, context=self.context).data