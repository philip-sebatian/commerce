from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class AuctionListing(models.Model):
    
    item=models.CharField(max_length=64)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.CharField(max_length=64)
    listingprice=models.IntegerField()
    
class bid(models.Model):
    item=models.ForeignKey(AuctionListing,on_delete=models.CASCADE)
    bidding=models.IntegerField()
class comments(models.Model):
    item=models.ForeignKey(AuctionListing,on_delete=models.CASCADE)
    comments=models.CharField(max_length=200)
    comments_owner=models.ForeignKey(User,on_delete=models.CASCADE)