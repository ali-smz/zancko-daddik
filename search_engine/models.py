from django.db import models
from django.conf import settings


class SearchTermHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    search_term = models.CharField(max_length=255)
    search_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} searched for '{self.search_term}' on {self.search_date}"


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks")
    record_id = models.CharField(max_length=255)
    index = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'record_id', 'index')

    def __str__(self):
        return f"{self.user.username} - {self.record_id}"