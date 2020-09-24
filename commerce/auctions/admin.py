from django.contrib import admin

from auctions.models import *
# Register your models here.

admin.site.register(Auction_listing)
admin.site.register(Bids)
admin.site.register(Comments)
