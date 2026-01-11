from django.db import models


class URL(models.Model):
    name = models.CharField(max_length=255)
    address = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or self.address


class CheckResult(models.Model):
    url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name='checks')
    status_code = models.IntegerField()
    response_time_ms = models.FloatField()
    is_up = models.BooleanField(default=False)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.url} - {self.status_code} @ {self.checked_at}"
