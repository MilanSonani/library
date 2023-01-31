from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'role']


class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']

admin.site.register(User)
admin.site.register(Book)
admin.site.register(BorrowUserBook)