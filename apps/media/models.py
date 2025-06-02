from django.db import models

from config.settings import AUTH_USER_MODEL

class MediaFile(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="media_files")
    file_name = models.CharField(max_length=255)
    ipfs_hash = models.CharField(max_length=255, unique=True)
    file_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
