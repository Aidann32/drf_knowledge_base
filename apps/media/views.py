from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser

from .ipfs import upload_to_ipfs
from .models import MediaFile
from .serializers import MediaFileSerializer


class UploadMediaFileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Upload file to IPFS
            ipfs_hash = upload_to_ipfs(uploaded_file)

            # Save metadata to database
            media_file = MediaFile.objects.create(
                user=request.user,
                file_name=uploaded_file.name,
                ipfs_hash=ipfs_hash,
                file_type=uploaded_file.content_type
            )

            return Response(MediaFileSerializer(media_file).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListMediaFilesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        media_files = MediaFile.objects.filter(user=request.user)
        serializer = MediaFileSerializer(media_files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RetrieveUpdateDeleteMediaFileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, user, pk):
        try:
            return MediaFile.objects.get(user=user, pk=pk)
        except MediaFile.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        media_file = self.get_object(request.user, pk)
        if not media_file:
            return Response({"error": "Media file not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MediaFileSerializer(media_file)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        media_file = self.get_object(request.user, pk)
        if not media_file:
            return Response({"error": "Media file not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MediaFileSerializer(media_file, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        media_file = self.get_object(request.user, pk)
        if not media_file:
            return Response({"error": "Media file not found."}, status=status.HTTP_404_NOT_FOUND)

        media_file.delete()
        return Response({"message": "Media file deleted successfully."}, status=status.HTTP_204_NO_CONTENT)