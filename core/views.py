from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from .serializers import LeaderboardSerializer, RecordSerializer
from .models import Leaderboard, Record
from .utils import get_access_token, get_data, process_data


class LeaderboardList(generics.ListAPIView):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer


class LeaderboardDetail(generics.RetrieveAPIView):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    lookup_field = 'slug'


class RecordList(generics.ListAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer


class RecordDetail(generics.RetrieveAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    lookup_field = 'pk'
