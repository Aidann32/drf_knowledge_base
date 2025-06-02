from django.db import models
from django.conf import settings

class NFT(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="nfts"
    )
    token_id = models.CharField(max_length=255, unique=True)
    ipfs_hash = models.CharField(max_length=255, unique=True)
    metadata_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"NFT {self.token_id} ({self.user.username})"

