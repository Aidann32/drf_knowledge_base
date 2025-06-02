from django.urls import path
from .views import MintNFTAPIView, UserNFTListAPIView, NFTDetailAPIView

urlpatterns = [
    path("nft/mint/", MintNFTAPIView.as_view(), name="mint-nft"),
    path("nft/user/", UserNFTListAPIView.as_view(), name="user-nft-list"),
    path("nft/<str:token_id>/", NFTDetailAPIView.as_view(), name="nft-detail"),
]
