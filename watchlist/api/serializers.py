from rest_framework.serializers import SerializerMethodField
from rest_framework import serializers
from watchlist.models import *

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude =('watchlist',)
        # fields = "__all__"
        
    


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = WatchList
        fields = "__all__"
        

class StreamPlatformSerializer(serializers.ModelSerializer):
    # watchlist = WatchListSerializer(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    viewer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Subscription
        fields = "__all__"


class WishListSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(read_only=True)
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = WishList
        fields = "__all__"


class GetSuggestionsSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    platform=SerializerMethodField()
    custom_field = SerializerMethodField()
    class Meta:
        model = WatchList
        fields = ["id", "content_type", "title", "storyline", "active",
                  "avg_rating", 'custom_field', "number_rating", "created",  "platform", "likes_count"]
    
    def get_platform(self, obj):
        serializer_data = StreamPlatformSerializer(obj.platform).data
        return serializer_data
    
    def get_custom_field(self, obj):
        print("context", self.context)
