from django.utils.translation import gettext_lazy as _
from django.db import models
from django_extensions.db.models import TimeStampedModel

class Contest(TimeStampedModel):
    SCOREBOARD_VISIBLE = 'V'
    SCOREBOARD_AFTER_CONTEST = 'C'
    SCOREBOARD_AFTER_PARTICIPATION = 'P'
    SCOREBOARD_HIDDEN = 'H'
    SCOREBOARD_VISIBILITY = (
        (SCOREBOARD_VISIBLE, _('Visible')),
        (SCOREBOARD_AFTER_CONTEST, _('Hidden for duration of contest')),
        (SCOREBOARD_AFTER_PARTICIPATION, _('Hidden for duration of participation')),
        (SCOREBOARD_HIDDEN, _('Hidden permanently')),
    )

    ## ------------------------------- GENERAL
    key = models.CharField(
        max_length=40, verbose_name=_('contest id'), unique=True,
        validators=[RegexValidator('^[a-z0-9]+$', _('Contest id must be ^[a-z0-9]+$'))])
    name = models.CharField(
        max_length=200, verbose_name=_('contest name'), db_index=True)
    description = models.TextField(verbose_name=_('description'), blank=True)
    user_count = models.IntegerField(
        verbose_name=_('the amount of live participants'), default=0)

    ## ------------------------------- VISIBILITY
    authors = models.ManyToManyField(
        UserProfile, verbose_name=_('authors'),
        help_text=_('These users will be able to edit the contest.'),
        related_name='authored_contests')
    curators = models.ManyToManyField(
        Profile, verbose_name=_('curators'),
        help_text=_('These users will be able to edit the contest, but will not be '
                    'listed as authors.'),
        related_name='curated_contests', blank=True)
    testers = models.ManyToManyField(
        UserProfile, verbose_name=_('testers'),
        help_text=_('These users will be able to view the contest, but not edit it.'),
        blank=True, related_name='tested_contests')
    tester_see_scoreboard = models.BooleanField(
        verbose_name=_('testers see scoreboard'), default=False,
        help_text=_('If testers can see the scoreboard.'))
    tester_see_submissions = models.BooleanField(
        verbose_name=_('testers see submissions'), default=False,
        help_text=_('If testers can see in-contest submissions.'))
    spectators = models.ManyToManyField(
        UserProfile, verbose_name=_('spectators'),
        help_text=_('These users will be able to spectate the contest, but not see '
                    'the problems ahead of time.'),
        blank=True, related_name='spectated_contests')
    
    is_visible = models.BooleanField(
        verbose_name=_('publicly visible'), default=False,
        help_text=_('Should be set even for organization-private contests, where it '
                    'determines whether the contest is visible to members of the '
                    'specified organizations.'))

    view_contest_scoreboard = models.ManyToManyField(
        UserProfile, verbose_name=_('view contest scoreboard'), blank=True,
        related_name='view_contest_scoreboard',
        help_text=_('These users will be able to view the scoreboard.'))
    view_contest_submissions = models.ManyToManyField(
        UserProfile, verbose_name=_('can see contest submissions'),
        blank=True, related_name='view_contest_submissions',
        help_text=_('These users will be able to see in-contest submissions.'))
    scoreboard_visibility = models.CharField(
        verbose_name=_('scoreboard visibility'), default=SCOREBOARD_VISIBLE,
        max_length=1, help_text=_('Scoreboard visibility through the duration of the contest'),
        choices=SCOREBOARD_VISIBILITY)
    is_private = models.BooleanField(
        verbose_name=_('private to specific users'), default=False)
    private_contestants = models.ManyToManyField(
        UserProfile, blank=True, verbose_name=_('private contestants'),
        help_text=_('If non-empty, only these users may see the contest'),
        related_name='private_contestants+')
    hide_problem_tags = models.BooleanField(
        verbose_name=_('hide problem tags'),
        help_text=_('Whether problem tags should be hidden by default.'),
        default=False)
    hide_problem_authors = models.BooleanField(
        verbose_name=_('hide problem authors'),
        help_text=_('Whether problem authors should be hidden by default.'),
        default=False)
    is_organization_private = models.BooleanField(verbose_name=_('private to organizations'), default=False)
    organizations = models.ManyToManyField(Organization, blank=True, verbose_name=_('organizations'),
                                           help_text=_('If non-empty, only these organizations may see '
                                                       'the contest'))
    limit_join_organizations = models.BooleanField(verbose_name=_('limit organizations that can join'), default=False)
    join_organizations = models.ManyToManyField(Organization, blank=True, verbose_name=_('join organizations'),
                                                help_text=_('If non-empty, only these organizations may join '
                                                            'the contest'), related_name='join_only_contests')
    classes = models.ManyToManyField(Class, blank=True, verbose_name=_('classes'),
                                     help_text=_('If organization private, only these classes may see the contest'))
    access_code = models.CharField(
        verbose_name=_('access code'), blank=True, default='', max_length=255,
        help_text=_('An optional code to prompt contestants before they are allowed '
                    'to join the contest. Leave it blank to disable.'))
    banned_users = models.ManyToManyField(
        UserProfile, verbose_name=_('Banned users'), blank=True,
        help_text=_('Bans the selected users from joining this contest.'))
    ## ------------------------------- CONFIGS
    start_time = models.DateTimeField(verbose_name=_('start time'), db_index=True)
    end_time = models.DateTimeField(verbose_name=_('end time'), db_index=True)
    time_limit = models.DurationField(verbose_name=_('time limit'), blank=True, null=True)

    use_clarifications = models.BooleanField(verbose_name=_('Allow clarifications'),
        help_text=_('Allow participants to submit clarifications'),
        default=True)

    locked_after = models.DateTimeField(
        verbose_name=_('contest lock'), null=True, blank=True,
        help_text=_('Prevent submissions from this contest '
                    'from being rejudged after this date.'))
    points_precision = models.IntegerField(
        verbose_name=_('precision points'), default=3,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text=_('Number of digits to round points to.'))
    
    format_name = models.CharField(
        verbose_name=_('contest format'), default='default', max_length=32,
        choices=contest_format.choices(), help_text=_('The contest format module to use.'))

    format_config = JSONField(
        verbose_name=_('contest format configuration'), null=True, blank=True,
        help_text=_('A JSON object to serve as the configuration for the chosen contest format '
                    'module. Leave empty to use None. Exact format depends on the contest format '
                    'selected.'))
    run_pretests_only = models.BooleanField(
        verbose_name=_('run pretests only'),
        help_text=_('Whether judges should grade pretests only, versus all '
                    'testcases. Commonly set during a contest, then unset '
                    'prior to rejudging user submissions when the contest ends.'),
        default=False)

    ## ------------------------------ RATING
    is_rated = models.BooleanField(
        verbose_name=_('contest rated'), help_text=_('Whether this contest can be rated.'),
        default=False)
    rating_floor = models.IntegerField(
        verbose_name=_('rating floor'), help_text=_('Rating floor for contest'),
        null=True, blank=True)
    rating_ceiling = models.IntegerField(
        verbose_name=_('rating ceiling'), help_text=_('Rating ceiling for contest'),
        null=True, blank=True)
    rate_all = models.BooleanField(
        verbose_name=_('rate all'), help_text=_('Rate all users who joined.'), default=False)
    rate_exclude = models.ManyToManyField(
        UserProfile, verbose_name=_('exclude from ratings'), blank=True,
        related_name='rate_exclude+')
    ## ------------------------------ DATA
    problems = models.ManyToManyField(Problem, verbose_name=_('problems'), through='ContestProblem')
    tags = models.ManyToManyField(
        ContestTag, verbose_name=_('contest tags'), blank=True, related_name='contests')
    ## ------------------------------ UNUSED
    show_short_display = models.BooleanField(
        verbose_name=_('show short form settings display'),
        help_text=_('Whether to show a section containing contest settings '
                    'on the contest page or not.'),
        default=False)
    og_image = models.CharField(
        verbose_name=_('OpenGraph image'), default='', max_length=150, blank=True)
    summary = models.TextField(
        blank=True, verbose_name=_('contest summary'),
        help_text=_('Plain-text, shown in meta description tag, e.g. for social media.'))
    logo_override_image = models.CharField(
        verbose_name=_('Logo override image'), default='', max_length=150,
        help_text=_('This image will replace the default site logo for users '
                    'inside the contest.'),
        blank=True,)
    problem_label_script = models.TextField(
        verbose_name=_('contest problem label script'), blank=True,
        help_text=_('A custom Lua function to generate problem labels. Requires a '
                    'single function with an integer parameter, the zero-indexed '
                    'contest problem index, and returns a string, the label.'))
    
    ## ------------------------------ Method
    @cached_property
    def format_class(self):
        return contest_format.formats[self.format_name]

    @cached_property
    def format(self):
        return self.format_class(self, self.format_config)

    @cached_property
    def get_label_for_problem(self):
        if not self.problem_label_script:
            return self.format.get_label_for_problem

        def DENY_ALL(obj, attr_name, is_setting):
            raise AttributeError()
        lua = LuaRuntime(attribute_filter=DENY_ALL, register_eval=False, register_builtins=False)
        return lua.eval(self.problem_label_script)

    def clean(self):
        # Django will complain if you didn't fill in start_time or end_time, so we don't have to.
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError('What is this? A contest that ended before it starts?')
        self.format_class.validate(self.format_config)

        try:
            # a contest should have at least one problem, with contest problem index 0
            # so test it to see if the script returns a valid label.
            label = self.get_label_for_problem(0)
        except Exception as e:
            raise ValidationError('Contest problem label script: %s' % e)
        else:
            if not isinstance(label, str):
                raise ValidationError('Contest problem label script: script should return a string.')

    def is_in_contest(self, user):
        if user.is_authenticated:
            profile = user.profile
            return profile and profile.current_contest is not None and profile.current_contest.contest == self
        return False

    def can_see_own_scoreboard(self, user):
        if self.can_see_full_scoreboard(user):
            return True
        if not self.started:
            return False
        if not self.show_scoreboard and not self.is_in_contest(user) and not self.has_completed_contest(user):
            return False
        return True

    def can_see_full_scoreboard(self, user):
        if self.show_scoreboard:
            return True
        if not user.is_authenticated:
            return False
        if user.has_perm('judge.see_private_contest') or user.has_perm('judge.edit_all_contest'):
            return True
        if user.profile.id in self.editor_ids:
            return True
        if self.tester_see_scoreboard and user.profile.id in self.tester_ids:
            return True
        if self.started and user.profile.id in self.spectator_ids:
            return True
        if self.view_contest_scoreboard.filter(id=user.profile.id).exists():
            return True
        if self.scoreboard_visibility == self.SCOREBOARD_AFTER_PARTICIPATION and self.has_completed_contest(user):
            return True
        return False

    def has_completed_contest(self, user):
        if user.is_authenticated:
            participation = self.users.filter(virtual=ContestParticipation.LIVE, user=user.profile).first()
            if participation and participation.ended:
                return True
        return False

    @cached_property
    def show_scoreboard(self):
        if not self.started:
            return False
        if (self.scoreboard_visibility in (self.SCOREBOARD_AFTER_CONTEST, self.SCOREBOARD_AFTER_PARTICIPATION) and
                not self.ended):
            return False
        return self.scoreboard_visibility != self.SCOREBOARD_HIDDEN

    @property
    def contest_window_length(self):
        return self.end_time - self.start_time

    @cached_property
    def _now(self):
        # This ensures that all methods talk about the same now.
        return timezone.now()

    @cached_property
    def started(self):
        return self.start_time <= self._now

    @property
    def time_before_start(self):
        if self.start_time >= self._now:
            return self.start_time - self._now
        else:
            return None

    @property
    def time_before_end(self):
        if self.end_time >= self._now:
            return self.end_time - self._now
        else:
            return None

    @cached_property
    def ended(self):
        return self.end_time < self._now

    @cached_property
    def author_ids(self):
        return Contest.authors.through.objects.filter(contest=self).values_list('profile_id', flat=True)

    @cached_property
    def editor_ids(self):
        return self.author_ids.union(
            Contest.curators.through.objects.filter(contest=self).values_list('profile_id', flat=True))

    @cached_property
    def tester_ids(self):
        return Contest.testers.through.objects.filter(contest=self).values_list('profile_id', flat=True)

    @cached_property
    def spectator_ids(self):
        return Contest.spectators.through.objects.filter(contest=self).values_list('profile_id', flat=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('contest_view', args=(self.key,))

    def update_user_count(self):
        self.user_count = self.users.filter(virtual=0).count()
        self.save()

    update_user_count.alters_data = True

    class Inaccessible(Exception):
        pass

    class PrivateContest(Exception):
        pass

    def access_check(self, user):
        # Do unauthenticated check here so we can skip authentication checks later on.
        if not user.is_authenticated:
            # Unauthenticated users can only see visible, non-private contests
            if not self.is_visible:
                raise self.Inaccessible()
            if self.is_private or self.is_organization_private:
                raise self.PrivateContest()
            return

        # If the user can view or edit all contests
        if user.has_perm('judge.see_private_contest') or user.has_perm('judge.edit_all_contest'):
            return

        # User is organizer or curator for contest
        if user.profile.id in self.editor_ids:
            return

        # User is tester for contest
        if user.profile.id in self.tester_ids:
            return

        # User is spectator for contest
        if user.profile.id in self.spectator_ids:
            return

        # Contest is not publicly visible
        if not self.is_visible:
            raise self.Inaccessible()

        # Contest is not private
        if not self.is_private and not self.is_organization_private:
            return

        if self.view_contest_scoreboard.filter(id=user.profile.id).exists():
            return

        in_org = (self.organizations.filter(id__in=user.profile.organizations.all()).exists() or
                  self.classes.filter(id__in=user.profile.classes.all()).exists())
        in_users = self.private_contestants.filter(id=user.profile.id).exists()

        if not self.is_private and self.is_organization_private:
            if in_org:
                return
            raise self.PrivateContest()

        if self.is_private and not self.is_organization_private:
            if in_users:
                return
            raise self.PrivateContest()

        if self.is_private and self.is_organization_private:
            if in_org and in_users:
                return
            raise self.PrivateContest()

    # Assumes the user can access, to avoid the cost again
    def is_live_joinable_by(self, user):
        if not self.started:
            return False

        if not user.is_authenticated:
            return False

        if user.profile.id in self.editor_ids or user.profile.id in self.tester_ids:
            return False

        if self.has_completed_contest(user):
            return False

        if self.limit_join_organizations:
            return self.join_organizations.filter(id__in=user.profile.organizations.all()).exists()
        return True

    # Also skips access check
    def is_spectatable_by(self, user):
        if not user.is_authenticated:
            return False

        if user.profile.id in self.editor_ids or user.profile.id in self.tester_ids:
            return True

        if self.limit_join_organizations:
            return self.join_organizations.filter(id__in=user.profile.organizations.all()).exists()
        return True

    def is_accessible_by(self, user):
        try:
            self.access_check(user)
        except (self.Inaccessible, self.PrivateContest):
            return False
        else:
            return True

    def is_editable_by(self, user):
        # If the user can edit all contests
        if user.has_perm('judge.edit_all_contest'):
            return True

        # If the user is a contest organizer or curator
        if user.has_perm('judge.edit_own_contest') and user.profile.id in self.editor_ids:
            return True

        return False

    @classmethod
    def get_visible_contests(cls, user):
        if not user.is_authenticated:
            return cls.objects.filter(is_visible=True, is_organization_private=False, is_private=False) \
                              .defer('description').distinct()

        queryset = cls.objects.defer('description')
        if not (user.has_perm('judge.see_private_contest') or user.has_perm('judge.edit_all_contest')):
            org_check = (Q(organizations__in=user.profile.organizations.all()) |
                         Q(classes__in=user.profile.classes.all()))
            q = Q(is_visible=True)
            q &= (
                Q(view_contest_scoreboard=user.profile) |
                Q(is_organization_private=False, is_private=False) |
                Q(is_organization_private=False, is_private=True, private_contestants=user.profile) |
                (Q(is_organization_private=True, is_private=False) & org_check) |
                (Q(is_organization_private=True, is_private=True, private_contestants=user.profile) & org_check)
            )

            q |= Q(authors=user.profile)
            q |= Q(curators=user.profile)
            q |= Q(testers=user.profile)
            q |= Q(spectators=user.profile)
            queryset = queryset.filter(q)
        return queryset.distinct()

    def rate(self):
        with transaction.atomic():
            Rating.objects.filter(contest__end_time__range=(self.end_time, self._now)).delete()
            for contest in Contest.objects.filter(
                is_rated=True, end_time__range=(self.end_time, self._now),
            ).order_by('end_time'):
                rate_contest(contest)

    class Meta:
        permissions = (
            ('see_private_contest', _('See private contests')),
            ('edit_own_contest', _('Edit own contests')),
            ('edit_all_contest', _('Edit all contests')),
            ('clone_contest', _('Clone contest')),
            ('moss_contest', _('MOSS contest')),
            ('contest_rating', _('Rate contests')),
            ('contest_access_code', _('Contest access codes')),
            ('create_private_contest', _('Create private contests')),
            ('change_contest_visibility', _('Change contest visibility')),
            ('contest_problem_label', _('Edit contest problem label script')),
            ('lock_contest', _('Change lock status of contest')),
        )
        verbose_name = _('contest')
        verbose_name_plural = _('contests')