from rest_framework import serializers
from compete.models import Contest
from problem.models import Problem
from userprofile.models import UserProfile
from userprofile.serializers import UserProfileSerializer

class ContestBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['key', 'start_time', 'end_time', 'name', 'authors', 'is_rated']

class ContestFullSerializer(serializers.ModelSerializer):
    authors = serializers.SlugRelatedField(
        many=True, slug_field='username',
        queryset=UserProfile.objects.all()
    )
    curators = serializers.SlugRelatedField(
        many=True, slug_field='username',
        queryset=UserProfile.objects.all()
    )
    spectators = serializers.SlugRelatedField(
        many=True, slug_field='username',
        queryset=UserProfile.objects.all()
    )
    problems = serializers.SlugRelatedField(
        many=True, slug_field='shortname',
        queryset=Problem.objects.all()
    )

    class Meta:
        model = Contest
        fields = [
            'key', 'name', 'authors', 
            'curators', 'spectators',
            'start_time', 'end_time', 
            'is_rated', 'problems', 
        ]