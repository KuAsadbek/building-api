from rest_framework.routers import DefaultRouter, APIRootView
from rest_framework.response import Response
from collections import OrderedDict

class CustomAPIRootView(APIRootView):
    def get(self, request, *args, **kwargs):
        base = request.build_absolute_uri

        return Response(OrderedDict({
            "dashboard": base("dashboard/"),
            "building": OrderedDict({
                "listing": base("listing/"),
                "listing-features": base("listing-features/"),
                "listing-nearby": base("listing-nearby/"),
                "listing-nearby-list": base("listing-nearby-list/"),
                "city": base("city/"),
                "district": base("district/"),
                "typesell": base("typesell/"),
                "category": base("category/"),
                "photo": base("photo/"),
            }),
            "interaction": OrderedDict({
                "rating": base("rating/"),
                "shares": base("shares/"),
                "views": base("views/"),
                "like": base("like/"),
                "favorites": base("favorites/"),
            }),
            "auth": OrderedDict({
                "users": base("users/"),
                "send_sms": base("send_sms/send-code/"),
                "verify-code": base("send_sms/verify-code/"),
                "register": base("auth/register/"),
                "login": base("auth/login/"),
            })
        }))

class CustomRouter(DefaultRouter):
    APIRootView = CustomAPIRootView