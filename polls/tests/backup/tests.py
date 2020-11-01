import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    """Create a question.

    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    """Unittests for Question Index View."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the index page."""
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed on the index page."""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions are displayed."""
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionModelTests(TestCase):
    """Unittests for Question Model."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """is_published() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(seconds=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_old_and_recent_question(self):
        """is_published() returns True for questions whose pub_date is in the older or within the last day."""
        old_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        new_time = timezone.now() - datetime.timedelta(seconds=1)
        old_question = Question(pub_date=old_time)
        new_question = Question(pub_date=new_time)
        self.assertIs(old_question.is_published(), True)
        self.assertIs(new_question.is_published(), True)

    def test_can_vote_with_no_end_date_question(self):
        """can_vote() returns True for questions without an end_date."""
        pub_time = timezone.now()
        end_time = None
        question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(question.can_vote(), True)

    def test_can_vote_not_passed_end_date_question(self):
        """can_vote() returns True for questions that have not passed the end_date."""
        pub_time = timezone.now()
        end_time = timezone.now() + timezone.timedelta(seconds=1)
        question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(question.can_vote(), True)

    def test_can_vote_passed_end_date_question(self):
        """can_vote() returns False for questions that have passed the end_date."""
        pub_time = timezone.now()
        end_time = timezone.now() + timezone.timedelta(seconds=1)
        question = Question(pub_date=pub_time, end_date=end_time)
        question.end_date -= timezone.timedelta(seconds=2)
        self.assertIs(question.can_vote(), False)

    def test_can_vote_before_pub_date_question(self):
        """can_vote() returns False for questions that are not published yet."""
        pub_time = timezone.now() + timezone.timedelta(seconds=1)
        end_time = None
        question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(question.can_vote(), False)
