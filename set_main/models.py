from django.db import models
from .choices_files import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.utils import timezone
from datetime import timedelta

class CurrencyRate(models.Model):
    CURRENCY_CHOICES = [
        ('USD', '🇺🇸 Доллар США'),
        ('RUB', '🇷🇺 Российский рубль'),
        ('UZS', '🇺🇿 Сум (базовая валюта)'),
    ]
    
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    rate = models.DecimalField(max_digits=12, decimal_places=4)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('currency', 'date')
        verbose_name = 'Курс валюты'
        verbose_name_plural = 'Курсы валют'

    def __str__(self):
        return f"{self.currency} - {self.rate} на {self.date}"


class PhoneConfirmation(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at + timedelta(minutes=3) < timezone.now()

    def __str__(self):
        return f"{self.phone} - {self.code}"

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.city.name} - {self.name}"

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Пользователь должен иметь номер телефона')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True)
    contact_phone = models.CharField(max_length=20, unique=True,blank=True, null=True)
    telegram = models.CharField(max_length=100, blank=True, null=True)
    whatsapp = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    language = models.CharField(max_length=3, choices=LANGUAGE_CHOICES, default='uz')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_busy = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

class TypeSell(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип объявления'
        verbose_name_plural = 'Типы объявлений'

class CategoryMod(models.Model):
    name_uz = models.CharField(max_length=100, unique=True)
    name_en = models.CharField(max_length=100, unique=True)
    name_ru = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class FeaturesCat(models.Model):
    title_uz = models.CharField(max_length=100, unique=True)
    title_en = models.CharField(max_length=100, unique=True)
    title_ru = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title_ru

class FeaturesMod(models.Model):
    listing = models.ForeignKey('ListingMod', on_delete=models.CASCADE)
    features = models.ForeignKey(FeaturesCat, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.listing.title}'

class NearbyMod(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class NearbyListMod(models.Model):
    listing = models.ForeignKey('ListingMod', on_delete=models.CASCADE)
    nearby = models.ForeignKey(NearbyMod, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.listing.title}'

class ListingMod(models.Model):
    TRANSACTION_TYPE_CHOICES = {
        ('sale', 'Продажа'),
        ('rent', 'Аренда'),
    }
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(CurrencyRate, on_delete=models.SET_NULL, null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    age = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    floor = models.PositiveIntegerField(null=True, blank=True)
    furnished = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    types = models.ForeignKey(TypeSell, on_delete=models.CASCADE, null=True,verbose_name='Тип недвижимости') #property_type
    category = models.ForeignKey(CategoryMod, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)
    video = models.FileField(upload_to='listing_videos/', blank=True, null=True)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPE_CHOICES, blank=True, null=True)
    mortgage_available = models.BooleanField(default=False) # ипотека
    created_at = models.DateTimeField(auto_now_add=True)

    is_promoted = models.BooleanField(default=False)
    promotion_expiry = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

class PhotoMod(models.Model):
    listing = models.ForeignKey(ListingMod, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='listing_photos/', blank=True, null=True)

    def __str__(self):
        return str(self.listing)

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

class RatingMod(models.Model):
    listing = models.ForeignKey(ListingMod, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.listing)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        ordering = ['-created_at']

class SharesMod(models.Model):
    listing = models.ForeignKey(ListingMod, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.listing)

    class Meta:
        verbose_name = 'Поделиться'
        verbose_name_plural = 'Поделиться'
        ordering = ['-created_at']

class ViewsMod(models.Model):
    listing = models.ForeignKey(ListingMod, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.listing)

    class Meta:
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'
        ordering = ['-created_at']

class LikeMod(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    listing = models.ForeignKey(ListingMod, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.listing)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        ordering = ['-created_at']

class FavoritesMod(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    listing = models.ForeignKey(ListingMod, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.listing)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        ordering = ['-created_at']