from django.urls import path

from .views import *

urlpatterns = [
    path('upload', UploadMediaFileAPIView.as_view(), name='upload-media-file'),
    path('', ListMediaFilesAPIView.as_view(), name='list-media-files'),
    path('<int:pk>', RetrieveUpdateDeleteMediaFileAPIView.as_view(), name='media-file-detail'),
]