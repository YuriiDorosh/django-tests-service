from django.db import models


class Test(models.Model):
    class STATUS(models.TextChoices):
        OK = "ok"
        ERROR = "error"

    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(
        max_length=12, choices=STATUS.choices, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tests"
        verbose_name = "Test"
        verbose_name_plural = "Tests"

    def __str__(self):
        return self.name
