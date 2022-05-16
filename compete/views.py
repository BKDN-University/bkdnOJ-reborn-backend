from django.shortcuts import get_object_or_404
from rest_framework import views, generics

from .models import Contest, ContestSubmission, ContestProblem
from .serializers import *

__all__ = ['ContestListView', 'ContestDetailView', 
    'ContestDetailProblemView', 'ContestDetailSubmissionView']

class ContestListView(generics.ListCreateAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestBasicSerializer
    permission_classes = []

class ContestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestFullSerializer
    permission_classes = []
    lookup_field = 'key'

class ContestDetailProblemView(generics.ListCreateAPIView):
    serializer_class = ContestProblemSerializer
    permission_classes = []
    lookup_field = 'key'

    def get_queryset(self):
        return ContestProblem.objects.all()

class ContestDetailSubmissionView(generics.ListCreateAPIView):
    serializer_class = ContestFullSerializer
    permission_classes = []
    lookup_field = 'key'

    def get_queryset(self):
        return ContestProblem.objects.all()