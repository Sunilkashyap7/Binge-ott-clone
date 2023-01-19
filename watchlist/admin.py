from django.contrib import admin

#Register your models here.
from watchlist.models import *


#Register your models here.

class WatchListAdmin(admin.ModelAdmin):
    readonly_fields = ('my_custom_field',)
    model = WatchList
    fields = ["MOVIE", "TV_SHOW", "content_type", "avg_rating", "number_rating", 'title', 'storyline', 'platform',
              'active',  'created', '', 'my_custom_field']
    list_display = ['title', "content_type",
                    'storyline', 'platform', 'my_custom_field']

    def my_custom_field(self, obj):
        return 'Return Anything Here'


admin.site.register(WatchList, WatchListAdmin)


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    fields = ['review_user', 'rating', 'description',
              'active']
    list_display = ['review_user', 'rating', 'description']


admin.site.register(Review, ReviewAdmin)


class ViewerAdmin(admin.ModelAdmin):
    model = Viewer
    fields = ['user', 'name', 'email',
              'age']
    list_display = ['user', 'name', 'email']


admin.site.register(Viewer, ViewerAdmin)


class WishListadmin(admin.ModelAdmin):
    readonly_fields = ['created', 'update',]
    model = WishList
    fields = ['wishlist_user', 'watchlist', 'active', 'created',
              'update']
    list_display = ['wishlist_user', 'watchlist']


admin.site.register(WishList, WishListadmin)


class Subscriptionadmin(admin.ModelAdmin):
    readonly_fields = ['created_at', ]
    model = Subscription
    list_display = ['viewer', 'created_at', 'is_paid', 'end_date']
    fields = ["viewer", "amount", 'days', 'created_at', 'is_paid',
              'end_date',  'is_active']


admin.site.register(Subscription, Subscriptionadmin)


class StreamPlatformAdmin(admin.ModelAdmin):
    model = StreamPlatform
    fields = ['name', 'about', 'website']
    list_display = ['name', 'about', 'website']

admin.site.register(StreamPlatform, StreamPlatformAdmin)
