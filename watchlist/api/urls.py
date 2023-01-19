from django.urls import path, include
from watchlist.api.views import *

urlpatterns = [
    
    path('stream/',StreamPlatformAV.as_view(), name ='stream-list'),
    path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='stream-detail'),
    path('list/', WatchListAV.as_view(), name='stream-detail'),
    path('list/<int:pk>/', WatchListDetailAV.as_view(), name='movie-detail'),
    path('stream/<int:pk>/review-create/',
         ReviewCreate.as_view(), name='review-create'),
    path('list2/', WatchListGV.as_view(), name='movie-list'),

    path('stream/<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('stream/review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('subscription/', SubscriptionAV.as_view(), name='subscription-detail'),
    path('wishlist/', WishListAV.as_view(), name='wish-list'),
    path('wishlist/<int:pk>/', WishListDetailAV.as_view(), name='wishlist-detail'),
    path('suggestions/', GetSuggestionsAV.as_view(), name='suggestion'),

]

