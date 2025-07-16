from django.contrib import admin
from .models import (
    CustomUser, TypeSell, CategoryMod, ListingMod, City, District,
    PhotoMod, RatingMod, SharesMod, ViewsMod,
    LikeMod, FavoritesMod, CommentMod,FeaturesCat,FeaturesMod,PhoneConfirmation
)

@admin.register(PhoneConfirmation)
class PhoneConfirmationModAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code')
    
@admin.register(FeaturesMod)
class FeaturesModAdmin(admin.ModelAdmin):
    list_display = ('listing', 'features')

@admin.register(FeaturesCat)
class FeaturesCatAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'title_en', 'title_ru')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ( 'phone', 'role', 'status', 'is_active')
    list_filter = ('role', 'status', 'is_active')
    search_fields = ('phone',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    list_filter = ('city',)
    search_fields = ('name',)

@admin.register(TypeSell)
class TypeSellAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(CategoryMod)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name_rub',)

@admin.register(ListingMod)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price_usd', 'city', 'district', 'status', 'created_at')
    list_filter = ('status', 'city', 'district', 'category')
    search_fields = ('title', 'description', 'user__username')
    autocomplete_fields = ('user',)

@admin.register(PhotoMod)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('listing', 'photo')

@admin.register(RatingMod)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'rating', 'created_at')

@admin.register(SharesMod)
class SharesAdmin(admin.ModelAdmin):
    list_display = ('listing', 'created_at')

@admin.register(ViewsMod)
class ViewsAdmin(admin.ModelAdmin):
    list_display = ('listing', 'created_at')

@admin.register(LikeMod)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'created_at')

@admin.register(FavoritesMod)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'created_at')

@admin.register(CommentMod)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'comment', 'created_at')
    search_fields = ('comment',)
