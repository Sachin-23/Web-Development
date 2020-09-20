from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


# for auction listing
class Auction_listing(models.Model):
    name = models.CharField(max_length=64) 
    description = models.CharField(max_length=256)
    initial_bid = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, \
            related_name="created_user")
    created_at = models.DateTimeField(auto_now_add=True)
    listing_url = models.URLField()
    active_listing = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.description} {self.initial_bid} \
                {self.user} {self.created_at} {self.listing_url}"

# for tracking category
class Category(models.Model):
    category = models.CharField(max_length=64) 
    item = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, \
            related_name="listing_category")
    def __str__(self):
        return f"{self.category} {self.item}"


# for bids
class Bids(models.Model):
    bid_user= models.ForeignKey(User, on_delete=models.CASCADE, \
            related_name="user_bid")
    bid_item = models.ForeignKey(Auction_listing, \
            on_delete=models.CASCADE, \
            related_name="item_bid")
    bid_value = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.bid_user} {self.bid_item} {self.bid_value}"

# for comments
class Comments(models.Model):
    comment_user = models.ForeignKey(User, \
            on_delete=models.CASCADE, \
            related_name="user_comment")
    comment_item = models.ForeignKey(Auction_listing, \
            on_delete=models.CASCADE, \
            related_name="item_comment")
    comment = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.comment_user} {self.comment_item} {self.comment}"


# for winners
class Winners(models.Model):
    winner_user = models.ForeignKey(User, on_delete=models.CASCADE, \
            related_name="winner")
    item = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, \
            related_name="winner_item")

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    item = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="watchlist_item")
