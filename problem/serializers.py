from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

from organization.models import Organization

from .models import Problem, ProblemTestProfile, TestCase
import logging
logger = logging.getLogger(__name__)


class ProblemBasicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Problem 
        fields = ['url', 'shortname', 'title']
        lookup_field = 'shortname'
        extra_kwargs = {
            'url': {'lookup_field': 'shortname'}
        }

class ProblemBriefSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Problem 
        fields = ['url', 'shortname', 'title', 'solved_count', 
            'attempted_count', 'points', 'is_published', 'is_privated_to_orgs']
        lookup_field = 'shortname'
        extra_kwargs = {
            'url': {'lookup_field': 'shortname'}
        }

# from judger.restful.serializers import LanguageSerializer
# The line above causes Circular Import, and I have been trying to fix 
# this for 30+ mins...
# Fuck it, lets redefine it for now. 
from judger.models import Language
class LanguageBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'key', 'name', 'short_name', 'common_name', 'ace']
        read_only_fields = ['id', 'key', 'name', 'short_name', 'common_name', 'ace']
        optional_fields = ['name', 'short_name', 'common_name', 'ace']
    
    def to_internal_value(self, data):
        if type(data) in [str, int]:
            lookup_key = ('key' if type(data) == str else 'id')
            langs = Language.objects.filter(**{f'{lookup_key}': data})
            if langs.exists():
                return langs[0].id

            raise serializers.ValidationError({
                'language_not_exist': f"Cannot find language with '{lookup_key}' = {data}"
            })
        else:
            return super().to_internal_value(data)


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    organizations = serializers.SlugRelatedField(
        queryset=Organization.objects.all(), many=True, slug_field="shortname", required=False 
    )
    authors = serializers.SlugRelatedField(
        queryset=User.objects.all(), many=True, slug_field="username", 
    )
    collaborators = serializers.SlugRelatedField(
        queryset=User.objects.all(), many=True, slug_field="username", required=False,
    )
    reviewers = serializers.SlugRelatedField(
        queryset=User.objects.all(), many=True, slug_field="username", required=False,
    )
    allowed_languages = LanguageBasicSerializer(many=True, required=False)

    class Meta:
        model = Problem 
        fields = [
            'url',
            'shortname', 'title', 'content', 'pdf',
            'source', 'time_limit', 'memory_limit',
            'authors', 'collaborators', 'reviewers',

            'allowed_languages',
            'is_published',
            'is_privated_to_orgs', 'organizations',
            'points', 'short_circuit', 'partial',

            'submission_visibility_mode', 'solved_count', 'attempted_count',
        ]
        read_only_fields = ['url', ]
        optional_fields = ['allowed_languages', 'collaborators', 'reviewers', 'organizations']
        lookup_field = 'shortname'
        extra_kwargs = {
            'url': {'lookup_field': 'shortname'},
        }
    
    def update(self, instance, validated_data):
        if validated_data.get('allowed_languages', None) != None:
            langs = validated_data.pop('allowed_languages')
            instance.allowed_languages.set(langs)
        return super().update(instance, validated_data)

class ProblemTestProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProblemTestProfile
        # fields = '__all__'
        exclude = ('output_prefix', 'output_limit')
        read_only_fields = ('problem', 'created', 'modified', 'feedback')#'zipfile', 'generator')
        lookup_field = 'problem'
        extra_kwargs = {
            'url': {'lookup_field': 'problem'}
        }
    
class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'
