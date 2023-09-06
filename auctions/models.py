from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class AuctionListing(models.Model):
    
    item=models.CharField(max_length=64)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.CharField(max_length=64)
    listingprice=models.IntegerField()
    img=models.URLField()
    status=models.CharField(default="active",max_length=7)
    
class bid(models.Model):
    item=models.ForeignKey(AuctionListing,on_delete=models.CASCADE)
    bidding=models.IntegerField()
    highestbider=models.ForeignKey(User,on_delete=models.CASCADE)
class comments(models.Model):
    item=models.ForeignKey(AuctionListing,on_delete=models.CASCADE)
    comments=models.CharField(max_length=200)
    comments_owner=models.ForeignKey(User,on_delete=models.CASCADE)

class watchlist(models.Model):
    item=models.ForeignKey(AuctionListing,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

class closelisting(models.Model):
    item=models.ForeignKey(AuctionListing,on_delete=models.CASCADE,related_name="bidq")
    winner=models.ForeignKey(User,on_delete=models.CASCADE)