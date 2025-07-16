from drf_spectacular.utils import extend_schema, extend_schema_view,OpenApiResponse
from ..serializer import (
    ListingSerializer,CategorySerializer,TypeSellSerializer,
    CitySerializer,DistrictSerializer,PhotoSerializer,
    FeaturesCatSerializer,FeaturesSerializer,
    RatingSerializer,SharesSerializer,ViewsSerializer,LikeSerializer,
    FavoritesSerializer,CommentSerializer,
    NearbySerializer,NearbyListSerializer
)

nearby_list_doc = extend_schema_view(
    list=extend_schema(
        summary="Nearby list",
        description="Returns all nearby.",
        responses={200: NearbyListSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve nearby by ID",
        responses={200: NearbyListSerializer}
    ),
    create=extend_schema(
        summary="Create a new nearby",
        request=NearbyListSerializer,
        responses={201: NearbyListSerializer}
    ),
    update=extend_schema(
        summary="Update a nearby",
        request=NearbyListSerializer,
        responses={200: NearbyListSerializer}
    ),
    partial_update=extend_schema(
        summary="Partially update a nearby",
        request=NearbyListSerializer,
        responses={200: NearbyListSerializer}    
    ),
    destroy=extend_schema(
        summary="Delete a nearby",
        responses={204: None}
    )
)

nearby_doc = extend_schema_view(
    list=extend_schema(
        summary="Nearby list",
        description="Returns all nearby.",
        responses={200: NearbySerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve nearby by ID",
        responses={200: NearbySerializer}
    ),
    create=extend_schema(
        summary="Create a new nearby",
        request=NearbySerializer,
        responses={201: NearbySerializer}
    ),
    update=extend_schema(
        summary="Update a nearby",
        request=NearbySerializer,
        responses={200: NearbySerializer}
    ),
    partial_update=extend_schema(
        summary="Partially update a nearby",
        request=NearbySerializer,
        responses={200: NearbySerializer}    
    ),
    destroy=extend_schema(
        summary="Delete a nearby",
        responses={204: None}
    )
)

comment_doc = extend_schema_view(
    list=extend_schema(
        summary="Comment list",
        description="Returns all comments.",
        responses={200: CommentSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve comment by ID",
        responses={200: CommentSerializer}
    ),
    create=extend_schema(
        summary="Create a new comment",
        request=CommentSerializer,
        responses={201: CommentSerializer}
    ),
    update=extend_schema(
        summary="Update a comment",
        request=CommentSerializer,
        responses={200: CommentSerializer}
    ),
    partial_update=extend_schema(
        summary="Partially update a comment",
        request=CommentSerializer,
        responses={200: CommentSerializer}
    ),
    destroy=extend_schema(
        summary="Delete a comment",
        responses={204: None}
    ),
)

favorites_doc = extend_schema_view(
    list=extend_schema(
        summary="Favorites list",
        description="Returns all favorite listings.",
        responses={200: FavoritesSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve favorite by ID",
        responses={200: FavoritesSerializer}
    ),
    create=extend_schema(
        summary="Add listing to favorites",
        request=FavoritesSerializer,
        responses={201: FavoritesSerializer}
    ),
    destroy=extend_schema(
        summary="Remove listing from favorites",
        responses={204: None}
    ),
    partial_update=extend_schema(
        summary="Update favorite",
        request=FavoritesSerializer,
        responses={200: FavoritesSerializer}
    ),
    update=extend_schema(
        summary="Update favorite",
        request=FavoritesSerializer,
        responses={200: FavoritesSerializer}
    )
)

like_doc = extend_schema_view(
    list=extend_schema(
        summary="Likes list",
        description="Returns all likes.",
        responses={200: LikeSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve like by ID",
        responses={200: LikeSerializer}
    ),
    create=extend_schema(
        summary="Add a like",
        request=LikeSerializer,
        responses={201: LikeSerializer}
    ),
    destroy=extend_schema(
        summary="Remove a like",
        responses={204: None}
    ),
    partial_update=extend_schema(
        summary="Update like",
        request=LikeSerializer,
        responses={200: LikeSerializer}
    ),
    update=extend_schema(
        summary="Update like",
        request=LikeSerializer,
        responses={200: LikeSerializer}
    )
)

views_doc = extend_schema_view(
    list=extend_schema(
        summary="Views list",
        description="Returns all views.",
        responses={200: ViewsSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve view by ID",
        responses={200: ViewsSerializer}
    ),
    create=extend_schema(
        summary="Add a view",
        request=ViewsSerializer,
        responses={201: ViewsSerializer}
    ),
    destroy=extend_schema(
        summary="Delete a view",
        responses={204: None}
    ),
    partial_update=extend_schema(
        summary="Update a view",
        request=ViewsSerializer,
        responses={200: ViewsSerializer}
    ),
    update=extend_schema(
        summary="Update a view",
        request=ViewsSerializer,
        responses={200: ViewsSerializer}
    )
)

shares_doc = extend_schema_view(
    list=extend_schema(
        summary="Shares list",
        description="Returns all shares.",
        responses={200: SharesSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve share by ID",
        responses={200: SharesSerializer}
    ),
    create=extend_schema(
        summary="Add a share",
        request=SharesSerializer,
        responses={201: SharesSerializer}
    ),
    destroy=extend_schema(
        summary="Delete a share",
        responses={204: None}
    ),
    partial_update=extend_schema(
        summary="Update a share",
        request=SharesSerializer,
        responses={200: SharesSerializer}
    ),
    update=extend_schema(
        summary="Update a share",
        request=SharesSerializer,
        responses={200: SharesSerializer}
    )
)

rating_doc = extend_schema_view(
    list=extend_schema(
        summary="Ratings list",
        description="Returns all ratings.",
        responses={200: RatingSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve rating by ID",
        responses={200: RatingSerializer}
    ),
    create=extend_schema(
        summary="Add a rating",
        request=RatingSerializer,
        responses={201: RatingSerializer}
    ),
    destroy=extend_schema(
        summary="Delete a rating",
        responses={204: None}
    ),
    partial_update=extend_schema(
        summary="Update a rating",
        request=RatingSerializer,
        responses={200: RatingSerializer}
    ),
    update=extend_schema(
        summary="Update a rating",
        request=RatingSerializer,
        responses={200: RatingSerializer}
    )
)

photo_doc = extend_schema_view(
    list=extend_schema(
        summary="Photos list",
        description="Returns all photos.",
        responses={200: PhotoSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve photo by ID",
        responses={200: PhotoSerializer}
    ),
    create=extend_schema(
        summary="Add a photo",
        request=PhotoSerializer,
        responses={201: PhotoSerializer}
    ),
    destroy=extend_schema(
        summary="Delete a photo",
        responses={204: None}
    ),
    partial_update=extend_schema(
        summary="Update a photo",
        request=PhotoSerializer,
        responses={200: PhotoSerializer}
    ),
    update=extend_schema(
        summary="Update a photo",
        request=PhotoSerializer,
        responses={200: PhotoSerializer}
    )
)

district_doc = extend_schema_view(
    list=extend_schema(
        summary="Districts list",
        description="Returns all districts.",
        responses={200: DistrictSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve district by ID",
        responses={200: DistrictSerializer}
    ),
    create=extend_schema(
        summary="Add a district",
        request=DistrictSerializer,
        responses={201: DistrictSerializer}
    ),
    destroy=extend_schema(
        summary="Delete a district",
        responses={204: None}
    ),
    partial_update=extend_schema(
        summary="Update a district",
        request=DistrictSerializer,
        responses={200: DistrictSerializer}
    ),
    update=extend_schema(
        summary="Update a district",
        request=DistrictSerializer,
        responses={200: DistrictSerializer}
    )
)

city_doc = extend_schema_view(
    list=extend_schema(
        summary="Cities list",
        description="Returns all cities.",
        responses={200: CitySerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve city by ID",
        responses={200: CitySerializer}
    ),
    create=extend_schema(
        summary="Add a city",
        request=CitySerializer,
        responses={201: CitySerializer}
    ),
    destroy=extend_schema(
        summary="Delete a city",
        responses={204: None}
    ),
    partial_update=extend_schema(
        summary="Update a city",
        request=CitySerializer,
        responses={200: CitySerializer}
    ),
    update=extend_schema(
        summary="Update a city",
        request=CitySerializer,
        responses={200: CitySerializer}
    )
)

typesell_doc = extend_schema_view(
    list=extend_schema(
        summary="Sell types list",
        description="Returns all types of sale.",
        responses={200: TypeSellSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve sell type by ID",
        responses={200: TypeSellSerializer}
    ),
    create=extend_schema(
        summary="Add a sell type",
        request=TypeSellSerializer,
        responses={201: TypeSellSerializer}
    ),
    destroy=extend_schema(
        summary="Delete a sell type",
        responses={204: None}
    ),
    partial_update=extend_schema(
        summary="Update a sell type",
        request=TypeSellSerializer,
        responses={200: TypeSellSerializer}
    ),
    update=extend_schema(
        summary="Update a sell type",
        request=TypeSellSerializer,
        responses={200: TypeSellSerializer}
    )
)

category_doc = extend_schema_view(
    list=extend_schema(
        summary="Categories list",
        description="Returns all categories.",
        responses={200: CategorySerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve category by ID",
        responses={200: CategorySerializer}
    ),
    create=extend_schema(
        summary="Add a category",
        request=CategorySerializer,
        responses={201: CategorySerializer}
    ),
    destroy=extend_schema(
        summary="Delete a category",
        responses={204: None}
    ),
    partial_update=extend_schema(
        summary="Update a category",
        request=CategorySerializer,
        responses={200: CategorySerializer}
    ),
    update=extend_schema(
        summary="Update a category",
        request=CategorySerializer,
        responses={200: CategorySerializer}
    )
)

listing_doc = extend_schema_view(
    list=extend_schema(
        summary="Listings list",
        description="Returns all listings.",
        responses={200: ListingSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve listing by ID",
        responses={200: ListingSerializer}
    ),
    create=extend_schema(
        summary="Add a new listing",
        request=ListingSerializer,
        responses={201: ListingSerializer}
    ),
    destroy=extend_schema(
        summary="Delete a listing",
        responses={204: None}
    ),
    partial_update=extend_schema(
        summary="Update a listing (partial)",
        request=ListingSerializer,
        responses={200: ListingSerializer}
    ),
    update=extend_schema(
        summary="Update a listing",
        request=ListingSerializer,
        responses={200: ListingSerializer}
    )
)

features_doc = extend_schema_view(
    list=extend_schema(
        summary="Features list",
        description="Returns all features.",
        responses={200: FeaturesSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve feature by ID",
        responses={200: FeaturesSerializer}
    ),
    create=extend_schema(
        summary="Add a feature",
        request=FeaturesSerializer,
        responses={201: FeaturesSerializer}
    ),
    destroy=extend_schema(
        summary="Delete a feature",
        responses={204: None}
    ),
    partial_update=extend_schema(
        summary="Update a feature",
        request=FeaturesSerializer,
        responses={200: FeaturesSerializer}
    ),
    update=extend_schema(
        summary="Update a feature",
        request=FeaturesSerializer,
        responses={200: FeaturesSerializer}
    )
)

features_cat_doc = extend_schema_view(
    list=extend_schema(
        summary="Feature categories list",
        description="Returns all feature categories.",
        responses={200: FeaturesCatSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve feature category by ID",
        responses={200: FeaturesCatSerializer}
    ),
    create=extend_schema(
        summary="Add a feature category",
        request=FeaturesCatSerializer,
        responses={201: FeaturesCatSerializer}
    ),
    destroy=extend_schema(
        summary="Delete a feature category",
        responses={204: None}
    ),
    partial_update=extend_schema(
        summary="Update a feature category",
        request=FeaturesCatSerializer,
        responses={200: FeaturesCatSerializer}
    ),
    update=extend_schema(
        summary="Update a feature category",
        request=FeaturesCatSerializer,
        responses={200: FeaturesCatSerializer}
    )
)

# Custom action docs

promote_doc = extend_schema(
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