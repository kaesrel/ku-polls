import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended', default=None, null=True)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """returns true if current date is on
        or after question’s publication date"""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """returns true if voting is
        currently allowed for this question"""
        now = timezone.now()
        return self.is_published() and \
               (self.end_date is None or now < self.end_date)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return  self.choice_text

    class Meta:
        ordering = ['-votes']
