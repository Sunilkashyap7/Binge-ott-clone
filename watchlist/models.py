from django.utils import timezone
from django.db import models
from user_app.models import User
from datetime import datetime, timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import *




class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField( max_length=150)
    website = models.URLField(max_length=100)
    
    def __str__(self):
        return self.name
    

@receiver(post_save, sender=StreamPlatform)
def StreamPlatform_post_save(sender, instance, created, *args, **kwargs):
    """
    after saved in the databse
    """
    if created:
        print("Streamplatform", instance.name)

        # trigger pre_save
        instance.save()
        # trigger post_save

    else:
        print(instance.name, "was just saved")
    
class Viewer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="Viewer")
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    age = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name) + "---" + str(self.user.id)

class WatchList(models.Model):
    MOVIE = 'M'
    TV_SHOW = 'T'
    CONTENT_TYPE_CHOICES = (
        (MOVIE, 'Movie'),
        (TV_SHOW, 'TV Show'),
    )
    content_type = models.CharField(
        max_length=1,
        choices=CONTENT_TYPE_CHOICES,
        default=MOVIE,
    )
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    platform = models.ForeignKey(
        StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")
    active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    review_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='review', null=True, blank=True)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    description = models.CharField(max_length=200, null=True)
    watchlist = models.ForeignKey(WatchList, on_delete = models.CASCADE, related_name='reviews',default=None)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating)  + "---" + str(self.watchlist.title)


class WishList(models.Model):
    wishlist_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="wishlist")
    watchlist = models.ForeignKey(
        WatchList, on_delete=models.CASCADE, related_name='wishlists')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.wishlist_user) + " | " + str(self.watchlist.title)
    

class Subscription(models.Model):
    viewer = models.ForeignKey(Viewer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    days = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=True, blank=True, null=True)
    end_date = models.DateField(
        default=datetime.today() + timedelta(days=30))
    days = models.IntegerField(null=True, blank=True)
      
    def __str__(self):
        return str(self.viewer)








#signals
# @receiver(pre_save, sender = User)
# def user_pre_save_receiver(sender, instance, *args, **kwargs):
#     """
#     befor saved in the databse
#     """

#     print(instance.email, instance.id) #None
#     #trigger pre_save
#     # DoNT DO THIS->  instance.save()
#     #trigger post_save


# @receiver(post_save, sender=User)
# def user_post_save_receiver(sender, instance, created, *args, **kwargs):
#     """
#     after saved in the databse
#     """
#     if created:
#         print("Send email to", instance.email)

#         # trigger pre_save
#         instance.save()
#         # trigger post_save

#     else:
#         print(instance.username,  "was just saved")


# @receiver(pre_delete, sender=User)
# def user_pre_delete(sender, instance, *args, **kwargs):
#     """
#     befor saved in the databse
#     """
#     print(f"{instance.username} will be removed")


# 2nd method
# pre_delete.connect(user_pre_delete, sender=User)


# @receiver(post_delete, sender=User)
# def user_post_delete(sender, instance, *args, **kwargs):
#     """
#     befor saved in the databse
#     """
#     print(f"{instance.username} has removed")
