from django.contrib import admin

from . models import (UserProfile, 
	Memberships,
	UserMembership,
	Subscription,
	Post)

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Memberships)
admin.site.register(UserMembership)
admin.site.register(Subscription)
admin.site.register(Post)

