from django.contrib import admin
from .models import News, Attachment, Order
from celery import shared_task
import time


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'created_at', 'slug', ]
    search_fields = ['title', 'text']
    list_filter = ['created_at', ]


@shared_task()
def update_status(instance_ids):
    time.sleep(10)
    queryset = Order.objects.filter(id__in=instance_ids)
    queryset.update(status=Order.Obrabotka)


def send_in_treatment(modeladmin, request, queryset):
    instance_ids = [instance.id for instance in queryset]
    update_status.delay(instance_ids)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['identification_number', 'description', 'sender', 'status', ]
    search_fields = ['identification_number', 'description']
    list_filter = ['status', ]
    actions = [send_in_treatment]
    send_in_treatment.short_description = 'Отправить в Обработку'


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['file', 'order', ]
    search_fields = ['order__description', 'order__identification_number']
