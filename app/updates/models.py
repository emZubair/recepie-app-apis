from django.db import models
from django.conf import settings


def upload_update_iamge(instance, image_name):
    return f'updates/{instance.user}/{image_name}'


class UpdateModel(models.Model):
    """Updates Model"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content = models.CharField(max_length=128, blank=True, null=True)
    image = models.ImageField(
        upload_to=upload_update_iamge, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.content or "Content not yet set!"
