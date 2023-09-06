from django.contrib import admin
from .models import User,bid,comments,AuctionListing,watchlist,closelisting

# Register your models here.
admin.site.register(User)
admin.site.register(bid)
admin.site.register(comments)
admin.site.register(AuctionListing)
admin.site.register(watchlist)
admin.site.register(closelisting)