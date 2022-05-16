from rest_framework import serializers
from compete.models import Contest, ContestProblem, ContestSubmission
from problem.models import Problem

__all__ = ['ContestProblemSerializer', 'ContestSubmissionSerializer']

class ContestProblemSerializer(serializers.ModelSerializer):
    contest = serializers.SlugRelatedField(
        queryset=Contest.objects.all(), slug_field="key")
    problem = serializers.SlugRelatedField(
        queryset=Problem.objects.all(), slug_field="shortname")

    class Meta:
        model = ContestProblem
        fields = '__all__'

class ContestSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestSubmission
        fields = '__all__'