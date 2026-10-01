from django.db import models


class Photo(models.Model):
    image = models.ImageField(upload_to="photos/")
    caption = models.CharField(max_length=80, blank=True)
    date_text = models.CharField(max_length=40, blank=True, help_text="e.g. 'Summer 2024'")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"Photo {self.pk}"