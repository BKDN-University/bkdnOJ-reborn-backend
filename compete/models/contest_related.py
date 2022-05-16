from django.utils.translation import gettext_lazy as _
from django.db import models
from django_extensions.db.models import TimeStampedModel

from .contest import Contest

class ContestParticipation(TimeStampedModel):
    LIVE = 0
    SPECTATE = -1

    contest = models.ForeignKey(
        Contest, verbose_name=_('associated contest'), related_name='users', on_delete=CASCADE)
    user = models.ForeignKey(
        Profile, verbose_name=_('user'), related_name='contest_history', on_delete=CASCADE)
    real_start = models.DateTimeField(
        verbose_name=_('start time'), default=timezone.now, db_column='start')
    score = models.FloatField(
        verbose_name=_('score'), default=0, db_index=True)
    cumtime = models.PositiveIntegerField(
        verbose_name=_('cumulative time'), default=0)
    is_disqualified = models.BooleanField(
        verbose_name=_('is disqualified'), default=False,
        help_text=_('Whether this participation is disqualified.'))
    tiebreaker = models.FloatField(
        verbose_name=_('tie-breaking field'), default=0.0)
    virtual = models.IntegerField(
        verbose_name=_('virtual participation id'), default=LIVE,
        help_text=_('0 means non-virtual, otherwise the n-th virtual participation.'))
    format_data = JSONField(
        verbose_name=_('contest format specific data'), null=True, blank=True)

    def recompute_results(self):
        with transaction.atomic():
            self.contest.format.update_participation(self)
            if self.is_disqualified:
                self.score = -9999
                self.cumtime = 0
                self.tiebreaker = 0
                self.save(update_fields=['score', 'cumtime', 'tiebreaker'])
    recompute_results.alters_data = True

    def set_disqualified(self, disqualified):
        self.is_disqualified = disqualified
        self.recompute_results()
        if self.contest.is_rated and self.contest.ratings.exists():
            self.contest.rate()
        if self.is_disqualified:
            if self.user.current_contest == self:
                self.user.remove_contest()
            self.contest.banned_users.add(self.user)
        else:
            self.contest.banned_users.remove(self.user)
    set_disqualified.alters_data = True

    @property
    def live(self):
        return self.virtual == self.LIVE

    @property
    def spectate(self):
        return self.virtual == self.SPECTATE

    @cached_property
    def start(self):
        contest = self.contest
        return contest.start_time if contest.time_limit is None and (self.live or self.spectate) else self.real_start

    @cached_property
    def end_time(self):
        contest = self.contest
        if self.spectate:
            return contest.end_time
        if self.virtual:
            if contest.time_limit:
                return self.real_start + contest.time_limit
            else:
                return self.real_start + (contest.end_time - contest.start_time)
        return contest.end_time if contest.time_limit is None else \
            min(self.real_start + contest.time_limit, contest.end_time)

    @cached_property
    def _now(self):
        # This ensures that all methods talk about the same now.
        return timezone.now()

    @property
    def ended(self):
        return self.end_time is not None and self.end_time < self._now

    @property
    def time_remaining(self):
        end = self.end_time
        if end is not None and end >= self._now:
            return end - self._now

    def __str__(self):
        if self.spectate:
            return gettext('%s spectating in %s') % (self.user.username, self.contest.name)
        if self.virtual:
            return gettext('%s in %s, v%d') % (self.user.username, self.contest.name, self.virtual)
        return gettext('%s in %s') % (self.user.username, self.contest.name)

    class Meta:
        verbose_name = _('contest participation')
        verbose_name_plural = _('contest participations')

        unique_together = ('contest', 'user', 'virtual')

class ContestProblem(models.Model):
    problem = models.ForeignKey(
        Problem, verbose_name=_('problem'), related_name='contests', on_delete=CASCADE)
    contest = models.ForeignKey(
        Contest, verbose_name=_('contest'), related_name='contest_problems', on_delete=CASCADE)
    points = models.IntegerField(verbose_name=_('points'))
    partial = models.BooleanField(default=True, verbose_name=_('partial'))
    is_pretested = models.BooleanField(default=False, verbose_name=_('is pretested'))
    order = models.PositiveIntegerField(db_index=True, verbose_name=_('order'))
    output_prefix_override = models.IntegerField(verbose_name=_('output prefix length override'),
                                                 default=0, null=True, blank=True)
    max_submissions = models.IntegerField(
        verbose_name=_('max submissions'),
        help_text=_('Maximum number of submissions for this problem, '
                    'or leave blank for no limit.'),
        default=None, null=True, blank=True,
        validators=[MinValueOrNoneValidator(1, _('Why include a problem you '
                                                "can't submit to?"))])

    class Meta:
        unique_together = ('problem', 'contest')
        verbose_name = _('contest problem')
        verbose_name_plural = _('contest problems')
        ordering = ('order',)


class ContestSubmission(models.Model):
    submission = models.OneToOneField(
        Submission, verbose_name=_('submission'),
        related_name='contest', on_delete=CASCADE)
    problem = models.ForeignKey(
        ContestProblem, verbose_name=_('problem'), on_delete=CASCADE,
        related_name='submissions', related_query_name='submission')
    participation = models.ForeignKey(
        ContestParticipation, verbose_name=_('participation'), on_delete=CASCADE,
        related_name='submissions', related_query_name='submission')
    points = models.FloatField(default=0.0, verbose_name=_('points'))
    is_pretest = models.BooleanField(
        verbose_name=_('is pretested'),
        help_text=_('Whether this submission was ran only on pretests.'),
        default=False)

    class Meta:
        verbose_name = _('contest submission')
        verbose_name_plural = _('contest submissions')
