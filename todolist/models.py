from django.db import models
from mytodo.settings import AUTH_USER_MODEL


# Create your models here.

class Todo(models.Model):
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    complete = models.BooleanField(default=False)

