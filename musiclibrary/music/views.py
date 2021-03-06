from functools import partial
from django.http import Http404
from django.shortcuts import render
from .models import Song
from .serializers import SongSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class SongList(APIView):
    #gets and returns all songs from DB
    def get(self, request):
        song = Song.objects.all()
        serializer = SongSerializer(song, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #creates and returns new song to DB
    def post(self, request):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#class based views to access songs db
class SongsDetail(APIView):
    def get_object(self,pk):
        try:
            return Song.objects.get(pk = pk)
        except Song.DoesNotExist:
            raise Http404

    #gets one song by primary key
    def get(self, request, pk):
        song = self.get_object(pk)
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #updates a song accessed by PK
    def put(self, request, pk):
        song = self.get_object(pk)
        serializer = SongSerializer(song, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #deletes a song
    def delete(self, request, pk):
        song = self.get_object(pk)
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    #updates just the counter field of a song accessed by PK
    def patch(self, request, pk):
        song = self.get_object(pk)
        song.likes = song.likes + 1
        serializer = SongSerializer(song, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



# Self discussion for understanding