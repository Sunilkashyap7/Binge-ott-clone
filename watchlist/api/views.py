from django.db.models import Count
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from watchlist.models import *
from watchlist.api.serializers import *
from watchlist.api.pagination import WatchListPagination, WatchListLOPagination, WatchListCPagination



class StreamPlatformAV(APIView):
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class StreamPlatformDetailAV(APIView):
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListCPagination


class WatchListAV(APIView):
    def get(self, request):
        movie = WatchList.objects.all()
        serializer = WatchListSerializer(movie, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class WatchListDetailAV(APIView):
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Not found '}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def post(self, request, pk): 
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(
            watchlist=watchlist, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You already have a review this waatchlist")

        serializer.save(watchlist=watchlist, review_user=review_user)
    
class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    
class SubscriptionAV(APIView):
    def post(self, request):
        viewer_id = request.data.get('viewer')
        amount = request.data.get('amount')
        days = request.data.get('days')
        try:
            viewer_obj = Viewer.objects.get(id=viewer_id)
        except Exception as e:
            return Response({'status': 'failed', 'message': 'Viewer does not exist', })
        
        obj = Subscription.objects.create(
            viewer=viewer_obj, amount=amount, days=days,)
        serializer_data = SubscriptionSerializer(obj).data
        return Response({'status': 'success', 'message': 'Data saved successfully', "data": serializer_data})
        
class WishListAV(APIView):
    def get(self, request):
        wishlist = WishList.objects.all()
        serializer = WishListSerializer(wishlist, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WishListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        else:
            return(serializer.errors) 
        
class WishListDetailAV(APIView):
    def get(self, request, pk):
        try:
            wishlist = WishList.objects.get(pk=pk)
        except WishList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WishListSerializer(wishlist)
        return Response(serializer.data)
    
    def put(self, request, pk):
        wishlist = WishList.objects.get(pk=pk)
        serializer = WishListSerializer(wishlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        Wishlist = WishList.objects.get(pk=pk)
        Wishlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetSuggestionsAV(APIView):
    def get(self, request):
        viewer_id = request.query_params.get('viewer')
        print(f'176----------------{viewer_id}')
        try:
            viewer_obj = Viewer.objects.get(id=viewer_id)

        except Exception as e:
            print(f'179---------------({e})')
            return Response({'status': 'failed', 'message': 'Viewer does not exist', })

        Subscription_obj = Subscription.objects.filter(
            viewer=viewer_obj, is_paid=True, is_active=True, end_date__gte=datetime.today()).last()
        if Subscription_obj:
            suggestion = (WatchList.objects
                          .annotate(likes_count=Count('reviews__likes', distinct=True))
                          .order_by('-likes_count', '-created'))
            context ={
                'title' : 'sunil'
            }
            serializer = GetSuggestionsSerializer(
                suggestion, many=True, context=context)
            return Response(serializer.data)
        else:
            return Response({'status': 'failed', 'message': 'Viewer have not subscription ', })
            


    
    
    

        
        