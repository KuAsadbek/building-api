from rest_framework import serializers
from .models import (
    ListingMod, CategoryMod, TypeSell,FeaturesCat,
    FeaturesMod, City, District, PhotoMod, RatingMod, 
    SharesMod, ViewsMod, LikeMod, FavoritesMod, 
    NearbyListMod,NearbyMod,CustomUser,PhoneConfirmation
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class ConfirmRegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)
    language = serializers.ChoiceField(choices=['uz', 'ru', 'en'])
    code = serializers.CharField()

    def validate(self, attrs):
        phone = attrs['phone']
        code = attrs['code']

        try:
            conf = PhoneConfirmation.objects.get(phone=phone, code=code)
        except PhoneConfirmation.DoesNotExist:
            raise serializers.ValidationError("Неверный код подтверждения")

        if conf.is_expired():
            raise serializers.ValidationError("Код подтверждения истёк")

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            name=validated_data["name"],
            phone=validated_data["phone"],
            password=validated_data["password"],
            language=validated_data["language"],
        )
        PhoneConfirmation.objects.filter(phone=validated_data["phone"]).delete()
        return user


class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'name', 'phone', 'contact_phone',
            'telegram', 'whatsapp', 'language'
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    contacts = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'phone', 'role', 'status', 'language', 'contacts']

    def get_contacts(self, obj):
        return {
            'contact_phone': obj.contact_phone,
            'telegram': obj.telegram,
            'whatsapp': obj.whatsapp
        }

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['name', 'phone', 'password', 'language']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(phone=data['phone'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверный номер телефона или пароль")


class ListingSerializer(serializers.ModelSerializer):
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
                    'id',
                    'user','user_name','title',
                    'description','category','price','transaction_type','specs','features',
                    'mortgage_available','nearby_list','coordinates','status',
                    'photos','location','video',
                    'city','city_name',
                    'types','types_name',
                    'like_count','view_count','share_count',
                    'rating_count','favorite_count',
                    'created_at',
                ]
    
    def get_language(self):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return getattr(request.user, 'language', 'uz')
        return 'uz'
    
    def to_representation(self, instance) -> dict:
        """Удаляем comments, если это не retrieve-запрос"""
        rep = super().to_representation(instance)
        request = self.context.get("request")
        if request and hasattr(request, "parser_context"):
            view = request.parser_context.get("view", None)
            if view and getattr(view, "action", None) != "retrieve":
                rep.pop("comments", None)
        return rep

    def get_specs(self,obj) -> dict:
        context = {
            'area': obj.area,
            'age': obj.age,
            'rooms': obj.rooms,
            'floor': obj.floor,
            'bathrooms': obj.bathrooms,
            'toilets': obj.toilets,
            'furnished': obj.furnished,
            'parking': obj.parking
        }
        return context

    def get_coordinates(self, obj) -> dict:
        context = {
            'lat': obj.latitude,
            'lng': obj.longitude
        }
        return context

    def get_location(self, obj) -> dict:
        context = {
            'city_id': obj.district.city.id,
            'city_name': obj.district.city.name,
            'district_id': obj.district.id,
            'district': obj.district.name,
        }
        return context
    
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

    def get_price(self, obj) -> dict:
        lang = self.get_language()
        price = {
            'uz': obj.price_usd,
            'ru': obj.price_rub,
            'en': obj.price_uzs,
        }
        context = {
            'lang':lang,
            'price': price[lang]
        }
        return context
    
    def get_types_name(self,obj) -> str:
        return obj.types.name
    
    def get_city_name(self,obj) -> str:
        return obj.city.name
    
    def get_user_name(self,obj) -> str:
        return obj.user.name

    def get_photos(self, obj) -> list:
        return PhotoSerializer(obj.photomod_set.all(), many=True, context=self.context).data

class NearbyListSer(serializers.ModelSerializer):
    nearby_name = serializers.SerializerMethodField()
    class Meta:
        model = NearbyListMod
        fields = ['nearby_name',]

    def get_nearby_name(self,obj) -> str:
        return obj.nearby.name

class NearbyListSerializer(serializers.ModelSerializer):
    listing_name = serializers.SerializerMethodField()
    nearby_name = serializers.SerializerMethodField()
    class Meta:
        model = NearbyListMod
        fields = '__all__'
    
    def get_listing_name(self,obj) -> str:
        return obj.listing.title
    def get_nearby_name(self,obj) -> str:
        return obj.nearby.name

    

class NearbySerializer(serializers.ModelSerializer):
    class Meta:
        model = NearbyMod
        fields = '__all__'

class FeaturesCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturesCat
        fields = '__all__'

class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturesMod
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryMod
        fields = '__all__'

class TypeSellSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeSell
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    listing_name = serializers.SerializerMethodField()
    class Meta:
        model = PhotoMod
        fields = '__all__'
    
    def get_listing_name(self,obj) -> str:
        return obj.listing.title

class RatingSerializer(serializers.ModelSerializer):
    listing_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = RatingMod
        fields = '__all__'
    
    def get_listing_name(self,obj) -> str:
        return obj.listing.title
    
    def get_user_name(self,obj) -> str:
        return obj.user.name

class SharesSerializer(serializers.ModelSerializer):
    listing_name = serializers.SerializerMethodField()
    class Meta:
        model = SharesMod
        fields = '__all__'

    def get_listing_name(self,obj) -> str:
        return obj.listing.title

class ViewsSerializer(serializers.ModelSerializer):
    listing_name = serializers.SerializerMethodField()
    class Meta:
        model = ViewsMod
        fields = '__all__'
    def get_listing_name(self,obj) -> str:
        return obj.listing.title

class LikeSerializer(serializers.ModelSerializer):
    listing_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = LikeMod
        fields = '__all__'
    
    def get_listing_name(self,obj) -> str:
        return obj.listing.title
    
    def get_user_name(self,obj) -> str:
        return obj.user.name

class FavoritesSerializer(serializers.ModelSerializer):
    listing_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = FavoritesMod
        fields = '__all__'
    def get_listing_name(self,obj) -> str:
        return obj.listing.title
    
    def get_user_name(self,obj) -> str:
        return obj.user.name

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

