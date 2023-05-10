import re

from django.conf import settings
from django.db import models


class Jobs(models.Model):
    class TypeChoices(models.TextChoices):
        FULL_TIME = "full-time"
        PART_TIME = "part-time"

    name = models.CharField(max_length=150)
    type = models.CharField(max_length=10, choices=TypeChoices.choices)

    class Meta:
        db_table = "jobs"
        verbose_name_plural = "jobs"

    def __str__(self) -> str:
        return f"Job ID: {self.id}, name: {self.name}"


class JobHeaders(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name="headers")
    rich_title_text = models.CharField(max_length=255)
    rich_subtitle_text = models.CharField(max_length=255)

    class Meta:
        db_table = "job_headers"
        verbose_name_plural = "job_headers"

    def __str__(self) -> str:
        return f"{self.rich_title_text}"

    @property
    def plain_title_text(self) -> str:
        return re.search(">(.+)<", self.rich_title_text).group(1)


class Applications(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications"
    )

    class Meta:
        unique_together = ("job", "user")
        db_table = "applications"
        verbose_name_plural = "applications"

    def __str__(self) -> str:
        return f"Job ID: {self.job.id}, user ID: {self.user.id}"
