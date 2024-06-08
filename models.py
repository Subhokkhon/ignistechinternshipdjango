from django.db import models
# taskmanager/models.py
from django.db import models

class ScrapingJob(models.Model):
    job_id = models.UUIDField(primary_key=True)
    status = models.CharField(max_length=20, default='PENDING')
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
