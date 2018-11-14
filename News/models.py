import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

class News(models.Model):
    #hospital = models.ForeignKey(Hospital, related_name='news_user', on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user_created = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_created_news', on_delete=models.PROTECT)

@receiver(post_save, sender=News)
def create_news_UUID(sender, instance=None, created=False, **kwargs):
    if created:
        NewsUUID.objects.create(news=instance, news_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id)))

class NewsUUID(models.Model):
    news = models.OneToOneField(News, related_name='news_uuid', primary_key=True, on_delete=models.PROTECT)
    news_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)