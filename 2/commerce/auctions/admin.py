from django.contrib import admin
from .models import Listing, Bid, Categories

# Register your models here.
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Categories)
