from django.contrib import admin
from .models import UserModel, FriendshipRequestModel, PhotoModel


# Register your models here.
admin.site.register(UserModel)

admin.site.register(FriendshipRequestModel)
admin.site.register(PhotoModel)


class UserModelAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}

# admin.site.register(UserModel,UserModelAdmin)

# admin.site.register(MyUserManager)