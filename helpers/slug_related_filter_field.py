from rest_framework.serializers import SlugRelatedField
from django.db.models import Q

class SlugRelatedFilterField(SlugRelatedField):
    def __init__(self, filter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter = filter

    def get_queryset(self):
        return self.queryset.filter(**{self.filter : self.context[self.filter]})
