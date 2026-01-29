from django.db import models


class Banner(models.Model):
    """Banner model data structure."""
    image = models.ImageField(
        upload_to="banners/",
        null=False,
        blank=False,
    )
    alt = models.CharField(max_length=255, verbose_name="Name")

    def __str__(self):
        return self.alt
