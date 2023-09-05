from django.contrib import admin
from .models import User,bid,comments,AuctionListing

# Register your models here.
admin.site.register(User)
admin.site.register(bid)
admin.site.register(comments)
admin.site.register(AuctionListing)