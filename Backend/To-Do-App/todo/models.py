from django.db import models
from django.contrib.auth.models import User
import uuid


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class Todo(BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_todos")
