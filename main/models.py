from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings


class News(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='images/news', null=True, blank=True, default=None)
    created_at = models.DateTimeField(default=timezone.now, blank=True, db_index=True, editable=False)
    slug = models.SlugField(max_length=200, unique=True, editable=False)

    class Meta:
        ordering = ['-created_at', ]
        verbose_name_plural = 'News'

    def save(self, *args, **kwargs):
        if not self.id:
            slug = slugify(self.title)
            news = News.objects.filter(slug__contains=slug)
            if news.exists():  # make sure slug will be unique if it has same title
                last_news_id = news.first().id
                slug = f"{slug}-{last_news_id+1}"
            self.slug = slug
        super().save(*args, **kwargs)


class Order(models.Model):
    Obrabotka = 'Об'
    Otpravlen = 'От'
    STATUS_CHOICES = (
        (Obrabotka, 'Обработка'),
        (Otpravlen, 'Отправлен')
    )

    identification_number = models.CharField(max_length=6)
    description = models.TextField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=Otpravlen, editable=False)

    def __str__(self):
        return f"{self.identification_number}.{self.description}"


class Attachment(models.Model):
    file = models.FileField(upload_to='files')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='attachments')

    def __str__(self):
        return f"{self.order} file"
