from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = [
    path('contest/', 
        ContestListView().as_view(), 
        name='contest-list'
    ),

    path('contest/<str:key>/', 
        ContestDetailView.as_view(), 
        name='contest-detail'
    ),
    path('contest/<str:key>/problem', 
        ContestDetailProblemView.as_view(), 
        name='contest-detail-problem'
    ),
    path('contest/<str:key>/submission', 
        ContestDetailSubmissionView.as_view(), 
        name='contest-detail-submission'
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)