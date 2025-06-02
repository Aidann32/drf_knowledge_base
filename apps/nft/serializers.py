from rest_framework import serializers
from .models import NFT

class NFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFT
        fields = ["id", "user", "token_id", "ipfs_hash", "metadata_url", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
