from django.apps import AppConfig
from django.db import DatabaseError
from django.utils.translation import gettext_lazy


class JudgeAppConfig(AppConfig):
    name = 'judger'
    verbose_name = gettext_lazy('Judge Servers')

    def ready(self):
        # WARNING: AS THIS IS NOT A FUNCTIONAL PROGRAMMING LANGUAGE,
        #          OPERATIONS MAY HAVE SIDE EFFECTS.
        #          DO NOT REMOVE THINKING THE IMPORT IS UNUSED.
        # noinspection PyUnresolvedReferences
        # from . import signals, jinja2  # noqa: F401, imported for side effects

        from userprofile.models import UserProfile
        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            for user in User.objects.filter(profile=None):
                # These poor profileless users
                profile = UserProfile(owner=user)
                profile.save()
        except DatabaseError:
            pass
