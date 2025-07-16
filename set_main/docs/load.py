from drf_spectacular.utils import (
    extend_schema, extend_schema_view,OpenApiResponse,
    extend_schema_serializer,OpenApiExample,OpenApiRequest,
    OpenApiTypes
)
from ..serializer import (
    ListingSerializer,CategorySerializer,TypeSellSerializer,
    CitySerializer,DistrictSerializer,PhotoSerializer,
    FeaturesCatSerializer,FeaturesSerializer,
    RatingSerializer,SharesSerializer,ViewsSerializer,LikeSerializer,
    FavoritesSerializer,CommentSerializer,CustomUserSerializer,
    NearbySerializer,NearbyListSerializer,LoginSerializer,RegisterSerializer
)

login_doc = extend_schema_view(
    register=extend_schema(
        summary="Регистрация нового пользователя",
        description="Создаёт нового пользователя. Возвращает информацию о пользователе.",
        tags=["Auth"],
        request=OpenApiRequest(
            request=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    name="Пример тела запроса",
                    value={
                        "name": "John Doe",
                        "phone": "+9984567890",
                        "password": "password",
                        "language": "en || ru || uz"
                    },
                    request_only=True
                )
            ]
        ),
        responses={
            201: OpenApiResponse(
                response=dict,
                description="Успешная регистрация. Возвращает информацию о пользователе.",
                examples=[
                    OpenApiExample(
                        name="Успешная регистрация",
                        value={
                            "status": 'true',
                            "message": "yaratildi",
                            "data": {
                                "user": {
                                    "id": 7,
                                    "name": "John 22Doe",
                                    "phone": "+993532590",
                                    "role": "user",
                                    "status": "active",
                                    "language": "uz",
                                    "contacts": {
                                        "contact_phone": 'null',
                                        "telegram": 'null',
                                        "whatsapp": 'null'
                                    }
                                },
                                "access": "jwt_token",
                                "refresh": "jwt_token"
                            }
                        }
                    )
                ]
            )
        }
    ),
    
    login=extend_schema(
        summary="Вход в систему",
        description="Авторизация по номеру телефона и паролю. Возвращает JWT токены.",
        tags=["Auth"],
        request=OpenApiRequest(
            request=OpenApiTypes.OBJECT,
        examples=[
            OpenApiExample(
                name="Пример тела запроса",
                value={
                    "phone": "998546584",
                    "password": "Admin"
                })]),
        responses={
            200: OpenApiResponse(
                response=dict,
                description="Успешный вход. Возвращает токены.",
                examples=[
                    OpenApiExample(
                        name="Ошибка валидации",
                        value={
                            "status": 'true',
                            "message": "muvaffaqiyatli",
                            "data": {
                                "refresh": "jwt_token",
                                "access": "jwt_token",
                                "user": {
                                    "id": 3,
                                    "name": "Doe John",
                                    "phone": "+998546584",
                                    "role": "user",
                                    "status": "active",
                                    "language": "ru",
                                    "contacts": {
                                        "contact_phone": 'null',
                                        "telegram": 'null',
                                        "whatsapp": 'null'
                                    }
                                }
                            }
                        },
                        response_only=True
                    )
                ]
            ),
        }
    )
)

sms_doc = extend_schema_view(
    send_code=extend_schema(
        summary="Отправка SMS-кода подтверждения",
        description="Отправляет 6-значный код подтверждения на указанный номер телефона. Ограничение: не чаще 1 раза в минуту.",
        tags=["Auth"],
        request=OpenApiRequest(
            request=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    name="Пример запроса",
                    value={
                        "phone": "998901234567"
                    },
                    request_only=True
                )
            ]
        ),
        responses={
            200: OpenApiResponse(
                response=dict,
                description="Код успешно отправлен",
                examples=[
                    OpenApiExample(
                        name="Успешный ответ",
                        value={"detail": "Код отправлен"},
                        response_only=True
                    )
                ]
            ),
            400: OpenApiResponse(
                response=dict,
                description="Ошибка запроса",
                examples=[
                    OpenApiExample(
                        name="Номер не передан",
                        value={"detail": "Номер телефона обязателен"},
                        response_only=True
                    )
                ]
            ),
            429: OpenApiResponse(
                response=dict,
                description="Слишком частые запросы",
                examples=[
                    OpenApiExample(
                        name="Повторная отправка слишком рано",
                        value={"detail": "Код уже отправлен. Повторите через 1 минуту."},
                        response_only=True
                    )
                ]
            )
        }
    ),
    verify_code = extend_schema(
        summary="Подтверждение номера",
        description="Подтверждает код, отправленный на номер телефона",
        tags=["Auth"],
        request=OpenApiRequest(
            request=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    name="Пример запроса",
                    value={
                        "phone": "998901234567",
                        "code": "123456"
                    },
                    request_only=True
                )
            ]
        ),
        responses={
            201: OpenApiResponse(
                response=dict,
                description="Успешная регистрация",
                examples=[
                    OpenApiExample(
                        name="Успешный ответ",
                        value={
                            "detail": "Код подтверждён"
                        },
                        response_only=True
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Ошибка подтверждения",
                response=dict,
                examples=[
                    OpenApiExample(
                        name="Неверный или истёкший код",
                        value={"non_field_errors": ["Неверный код подтверждения"]},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="Код истёк",
                        value={"non_field_errors": ["Код подтверждения истёк"]},
                        response_only=True
                    )
                ]
            )
        }
    ),
)


# old doc

custom_user_doc = extend_schema_view(
    list=extend_schema(
        tags=["users"],
        summary="Users list",
        description="Returns all users.",
        responses={200: CustomUserSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["users"],
        summary="Retrieve user by ID",
        responses={200: CustomUserSerializer}
    ),
    create=extend_schema(
        tags=["users"],
        summary="Add a user",
        request=CustomUserSerializer,
        responses={201: CustomUserSerializer}
    ),
    destroy=extend_schema(
        tags=["users"],
        summary="Delete a user",
        responses={204: None}
    ),
    partial_update=extend_schema(
        tags=["users"],
        summary="Update a user",
        request=CustomUserSerializer,
        responses={200: CustomUserSerializer}
    ),
    update=extend_schema(
        tags=["users"],
        summary="Update a user",
        request=CustomUserSerializer,
        responses={200: CustomUserSerializer}
    )
)

nearby_list_doc = extend_schema_view(
    list=extend_schema(
        tags=["Building-listing"],
        summary="Nearby list",
        description="Returns all nearby.",
        responses={200: NearbyListSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["Building-listing"],
        summary="Retrieve nearby by ID",
        responses={200: NearbyListSerializer}
    ),
    create=extend_schema(
        tags=["Building-listing"],
        summary="Create a new nearby",
        request=NearbyListSerializer,
        responses={201: NearbyListSerializer}
    ),
    update=extend_schema(
        tags=["Building-listing"],
        summary="Update a nearby",
        request=NearbyListSerializer,
        responses={200: NearbyListSerializer}
    ),
    partial_update=extend_schema(
        tags=["Building-listing"],
        summary="Partially update a nearby",
        request=NearbyListSerializer,
        responses={200: NearbyListSerializer}    
    ),
    destroy=extend_schema(
        tags=["Building-listing"],
        summary="Delete a nearby",
        responses={204: None}
    )
)

nearby_doc = extend_schema_view(
    list=extend_schema(
        tags=["Building-listing"],
        summary="Nearby list",
        description="Returns all nearby.",
        responses={200: NearbySerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["Building-listing"],
        summary="Retrieve nearby by ID",
        responses={200: NearbySerializer}
    ),
    create=extend_schema(
        tags=["Building-listing"],
        summary="Create a new nearby",
        request=NearbySerializer,
        responses={201: NearbySerializer}
    ),
    update=extend_schema(
        tags=["Building-listing"],
        summary="Update a nearby",
        request=NearbySerializer,
        responses={200: NearbySerializer}
    ),
    partial_update=extend_schema(
        tags=["Building-listing"],
        summary="Partially update a nearby",
        request=NearbySerializer,
        responses={200: NearbySerializer}    
    ),
    destroy=extend_schema(
        tags=["Building-listing"],
        summary="Delete a nearby",
        responses={204: None}
    )
)

comment_doc = extend_schema_view(
    list=extend_schema(
        tags=["comments"],
        summary="Comment list",
        description="Returns all comment.",
        responses={200: CommentSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["comments"],
        summary="Retrieve comment by ID",
        responses={200: CommentSerializer}
    ),
    create=extend_schema(
        tags=["comments"],
        summary="Create a new comment",
        request=CommentSerializer,
        responses={201: CommentSerializer}
    ),
    update=extend_schema(
        tags=["comments"],
        summary="Update a comment",
        request=CommentSerializer,
        responses={200: CommentSerializer}
    ),
    partial_update=extend_schema(
        tags=["comments"],
        summary="Partially update a comment",
        request=CommentSerializer,
        responses={200: CommentSerializer}
    ),
    destroy=extend_schema(
        tags=["comments"],
        summary="Delete a comment",
        responses={204: None}
    ),
)

favorites_doc = extend_schema_view(
    list=extend_schema(
        tags=["favorites"],
        summary="Favorites list",
        description="Returns all favorite listings.",
        responses={200: FavoritesSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["favorites"],
        summary="Retrieve favorite by ID",
        responses={200: FavoritesSerializer}
    ),
    create=extend_schema(
        tags=["favorites"],
        summary="Add listing to favorites",
        request=FavoritesSerializer,
        responses={201: FavoritesSerializer}
    ),
    destroy=extend_schema(
        tags=["favorites"],
        summary="Remove listing from favorites",
        responses={204: None}
    ),
    partial_update=extend_schema(
        tags=["favorites"],
        summary="Update favorite",
        request=FavoritesSerializer,
        responses={200: FavoritesSerializer}
    ),
    update=extend_schema(
        tags=["favorites"],
        summary="Update favorite",
        request=FavoritesSerializer,
        responses={200: FavoritesSerializer}
    )
)

like_doc = extend_schema_view(
    list=extend_schema(
        tags=["likes"],
        summary="Likes list",
        description="Returns all likes.",
        responses={200: LikeSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["likes"],
        summary="Retrieve like by ID",
        responses={200: LikeSerializer}
    ),
    create=extend_schema(
        tags=["likes"],
        summary="Add a like",
        request=LikeSerializer,
        responses={201: LikeSerializer}
    ),
    destroy=extend_schema(
        tags=["likes"],
        summary="Remove a like",
        responses={204: None}
    ),
    partial_update=extend_schema(
        tags=["likes"],
        summary="Update like",
        request=LikeSerializer,
        responses={200: LikeSerializer}
    ),
    update=extend_schema(
        tags=["likes"],
        summary="Update like",
        request=LikeSerializer,
        responses={200: LikeSerializer}
    )
)

views_doc = extend_schema_view(
    list=extend_schema(
        tags=["views"],
        summary="Views list",
        description="Returns all views.",
        responses={200: ViewsSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["views"],
        summary="Retrieve view by ID",
        responses={200: ViewsSerializer}
    ),
    create=extend_schema(
        tags=["views"],
        summary="Add a view",
        request=ViewsSerializer,
        responses={201: ViewsSerializer}
    ),
    destroy=extend_schema(
        tags=["views"],
        summary="Delete a view",
        responses={204: None}
    ),
    partial_update=extend_schema(
        tags=["views"],
        summary="Update a view",
        request=ViewsSerializer,
        responses={200: ViewsSerializer}
    ),
    update=extend_schema(
        tags=["views"],
        summary="Update a view",
        request=ViewsSerializer,
        responses={200: ViewsSerializer}
    )
)

shares_doc = extend_schema_view(
    list=extend_schema(
        tags=["shares"],
        summary="Shares list",
        description="Returns all shares.",
        responses={200: SharesSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["shares"],
        summary="Retrieve share by ID",
        responses={200: SharesSerializer}
    ),
    create=extend_schema(
        tags=["shares"],
        summary="Add a share",
        request=SharesSerializer,
        responses={201: SharesSerializer}
    ),
    destroy=extend_schema(
        tags=["shares"],
        summary="Delete a share",
        responses={204: None}
    ),
    partial_update=extend_schema(
        tags=["shares"],
        summary="Update a share",
        request=SharesSerializer,
        responses={200: SharesSerializer}
    ),
    update=extend_schema(
        tags=["shares"],
        summary="Update a share",
        request=SharesSerializer,
        responses={200: SharesSerializer}
    )
)

rating_doc = extend_schema_view(
    list=extend_schema(
        tags=["ratings"],
        summary="Ratings list",
        description="Returns all ratings.",
        responses={200: RatingSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["ratings"],
        summary="Retrieve rating by ID",
        responses={200: RatingSerializer}
    ),
    create=extend_schema(
        tags=["ratings"],
        summary="Add a rating",
        request=RatingSerializer,
        responses={201: RatingSerializer}
    ),
    destroy=extend_schema(
        tags=["ratings"],
        summary="Delete a rating",
        responses={204: None}
    ),
    partial_update=extend_schema(
        tags=["ratings"],
        summary="Update a rating",
        request=RatingSerializer,
        responses={200: RatingSerializer}
    ),
    update=extend_schema(
        tags=["ratings"],
        summary="Update a rating",
        request=RatingSerializer,
        responses={200: RatingSerializer}
    )
)

photo_doc = extend_schema_view(
    list=extend_schema(
        tags=["photos"],
        summary="Photos list",
        description="Returns all photos.",
        responses={200: PhotoSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["photos"],
        summary="Retrieve photo by ID",
        responses={200: PhotoSerializer}
    ),
    create=extend_schema(
        tags=["photos"],
        summary="Add a photo",
        request=PhotoSerializer,
        responses={201: PhotoSerializer}
    ),
    destroy=extend_schema(
        tags=["photos"],
        summary="Delete a photo",
        responses={204: None}
    ),
    partial_update=extend_schema(
        tags=["photos"],
        summary="Update a photo",
        request=PhotoSerializer,
        responses={200: PhotoSerializer}
    ),
    update=extend_schema(
        tags=["photos"],
        summary="Update a photo",
        request=PhotoSerializer,
        responses={200: PhotoSerializer}
    )
)

district_doc = extend_schema_view(
    list=extend_schema(
        tags=["districts"],
        summary="Districts list",
        description="Returns all districts.",
        responses={200: DistrictSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["districts"],
        summary="Retrieve district by ID",
        responses={200: DistrictSerializer}
    ),
    create=extend_schema(
        tags=["districts"],
        summary="Add a district",
        request=DistrictSerializer,
        responses={201: DistrictSerializer}
    ),
    destroy=extend_schema(
        tags=["districts"],
        summary="Delete a district",
        responses={204: None}
    ),
    partial_update=extend_schema(
        tags=["districts"],
        summary="Update a district",
        request=DistrictSerializer,
        responses={200: DistrictSerializer}
    ),
    update=extend_schema(
        tags=["districts"],
        summary="Update a district",
        request=DistrictSerializer,
        responses={200: DistrictSerializer}
    )
)

city_doc = extend_schema_view(
    list=extend_schema(
        tags=["cities"],
        summary="Cities list",
        description="Returns all cities.",
        responses={200: CitySerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["cities"],
        summary="Retrieve city by ID",
        responses={200: CitySerializer}
    ),
    create=extend_schema(
        tags=["cities"],
        summary="Add a city",
        request=CitySerializer,
        responses={201: CitySerializer}
    ),
    destroy=extend_schema(
        tags=["cities"],
        summary="Delete a city",
        responses={204: None}
    ),
    partial_update=extend_schema(
        tags=["cities"],
        summary="Update a city",
        request=CitySerializer,
        responses={200: CitySerializer}
    ),
    update=extend_schema(
        tags=["cities"],
        summary="Update a city",
        request=CitySerializer,
        responses={200: CitySerializer}
    )
)

typesell_doc = extend_schema_view(
    list=extend_schema(
        tags=["typesells"],
        summary="Sell types list",
        description="Returns all types of sale.",
        responses={200: TypeSellSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["typesells"],
        summary="Retrieve sell type by ID",
        responses={200: TypeSellSerializer}
    ),
    create=extend_schema(
        tags=["typesells"],
        summary="Add a sell type",
        request=TypeSellSerializer,
        responses={201: TypeSellSerializer}
    ),
    destroy=extend_schema(
        tags=["typesells"],
        summary="Delete a sell type",
        responses={204: None}
    ),
    partial_update=extend_schema(
        tags=["typesells"],
        summary="Update a sell type",
        request=TypeSellSerializer,
        responses={200: TypeSellSerializer}
    ),
    update=extend_schema(
        tags=["typesells"],
        summary="Update a sell type",
        request=TypeSellSerializer,
        responses={200: TypeSellSerializer}
    )
)

category_doc = extend_schema_view(
    list=extend_schema(
        tags=["categories"],
        summary="Categories list",
        description="Returns all categories.",
        responses={200: CategorySerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["categories"],
        summary="Retrieve category by ID",
        responses={200: CategorySerializer}
    ),
    create=extend_schema(
        tags=["categories"],
        summary="Add a category",
        request=CategorySerializer,
        responses={201: CategorySerializer}
    ),
    destroy=extend_schema(
        tags=["categories"],
        summary="Delete a category",
        responses={204: None}
    ),
    partial_update=extend_schema(
        tags=["categories"],
        summary="Update a category",
        request=CategorySerializer,
        responses={200: CategorySerializer}
    ),
    update=extend_schema(
        tags=["categories"],
        summary="Update a category",
        request=CategorySerializer,
        responses={200: CategorySerializer}
    )
)

listing_doc = extend_schema_view(
    list=extend_schema(
        tags=["listings"],
        summary="Listings list",
        description="Returns all listings.",
        responses={200: ListingSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["listings"],
        summary="Retrieve listing by ID",
        responses={200: ListingSerializer}
    ),
    create=extend_schema(
        tags=["listings"],
        summary="Add a new listing",
        request=ListingSerializer,
        responses={201: ListingSerializer}
    ),
    destroy=extend_schema(
        tags=["listings"],
        summary="Delete a listing",
        responses={204: None}
    ),
    partial_update=extend_schema(
        tags=["listings"],
        summary="Update a listing (partial)",
        request=ListingSerializer,
        responses={200: ListingSerializer}
    ),
    update=extend_schema(
        tags=["listings"],
        summary="Update a listing",
        request=ListingSerializer,
        responses={200: ListingSerializer}
    )
)

features_doc = extend_schema_view(
    list=extend_schema(
        tags=["features"],
        summary="Features list",
        description="Returns all features.",
        responses={200: FeaturesSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["features"],
        summary="Retrieve feature by ID",
        responses={200: FeaturesSerializer}
    ),
    create=extend_schema(
        tags=["features"],
        summary="Add a feature",
        request=FeaturesSerializer,
        responses={201: FeaturesSerializer}
    ),
    destroy=extend_schema(
        tags=["features"],
        summary="Delete a feature",
        responses={204: None}
    ),
    partial_update=extend_schema(
        tags=["features"],
        summary="Update a feature",
        request=FeaturesSerializer,
        responses={200: FeaturesSerializer}
    ),
    update=extend_schema(
        tags=["features"],
        summary="Update a feature",
        request=FeaturesSerializer,
        responses={200: FeaturesSerializer}
    )
)

features_cat_doc = extend_schema_view(
    list=extend_schema(
        tags=["features"],
        summary="Feature categories list",
        description="Returns all feature categories.",
        responses={200: FeaturesCatSerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["features"],
        summary="Retrieve feature category by ID",
        responses={200: FeaturesCatSerializer}
    ),
    create=extend_schema(
        tags=["features"],
        summary="Add a feature category",
        request=FeaturesCatSerializer,
        responses={201: FeaturesCatSerializer}
    ),
    destroy=extend_schema(
        tags=["features"],
        summary="Delete a feature category",
        responses={204: None}
    ),
    partial_update=extend_schema(
        tags=["features"],
        summary="Update a feature category",
        request=FeaturesCatSerializer,
        responses={200: FeaturesCatSerializer}
    ),
    update=extend_schema(
        tags=["features"],
        summary="Update a feature category",
        request=FeaturesCatSerializer,
        responses={200: FeaturesCatSerializer}
    )
)

# Custom action docs

promote_doc = extend_schema(
    tags=["listings"],
    summary="Promote a listing",
    description="Promotes a listing for a specified number of days (default is 7 days).",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer",
                    "example": 7
                }
            },
            "required": ["days"]
        }
    },
    responses={
        200: OpenApiResponse(
            description="Listing successfully promoted",
            response={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Listing promoted for 7 days"
                    }
                }
            }
        )
    }
)