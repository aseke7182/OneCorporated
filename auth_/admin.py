from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def birthday(self, obj):
        return obj.birthday_date.strftime('%d.%m.%Y')

    list_display = ['email', 'name', 'created_at', 'birthday', 'is_staff', ]
    search_fields = ['email', 'name']
    list_filter = ['birthday_date', ]

