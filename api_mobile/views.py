import random
import string
from django.utils import timezone
from rest_framework import status
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,ViewSet

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .utils.mixins import CustomResponseMixin

from set_main.models import (
    ListingMod,CategoryMod,TypeSell,
    City,District,PhotoMod,
    FeaturesCat,FeaturesMod,
    RatingMod,SharesMod,ViewsMod,LikeMod,
    FavoritesMod,CustomUser,PhoneConfirmation,
    NearbyListMod,NearbyMod
)

from .serializer import (
    ListingMobSerializer
)

class ListingMobViewSet(CustomResponseMixin,ModelViewSet):
    queryset = ListingMod.objects.all()
    serializer_class = ListingMobSerializer