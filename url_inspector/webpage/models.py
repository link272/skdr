from django.db import models
from django.contrib.auth.models import User
import hashlib
import base64


def url_hasher(url):
    url_b64 = base64.urlsafe_b64encode(url.encode())
    return hashlib.sha256(url_b64).hexdigest()


class VisitedWebPage(models.Model):

    class Meta:
        index_together = ["url_hash", "user"]
        get_latest_by = "visited_at"

    url: str = models.URLField(max_length=2048)
    url_hash = models.CharField(max_length=256, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    visited_at = models.DateTimeField(auto_now_add=True)
    nb_http_link = models.PositiveIntegerField(default=0)
    nb_tel_link = models.PositiveIntegerField(default=0)
    nb_mail_link = models.PositiveIntegerField(default=0)

    def save(self, **kwargs):
        self.url_hash = url_hasher(self.url)
        return super().save(**kwargs)
