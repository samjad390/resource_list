import uuid
from django.db import models

from module.models import TimeStampModel


class ResourceNotes(TimeStampModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False)
    name = models.CharField(max_length=255)
    notes = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} - {self.email}"
