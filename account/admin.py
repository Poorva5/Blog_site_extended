from django.contrib import admin
from .models import UserData

@admin.register(UserData)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name',)
   


