from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from polls.models import Question, Choice


class VotingTest(TestCase):


    def setUp(self):
        voter = User.objects.create_user("Mag", "joe@his.domain", "jotaro")
        voter.first_name = "Magnus"
        voter.last_name = "Joestar"
        voter.save()

    def test_unauthenticated_vote(self):
        question = Question.objects.create(
                question_text="Do you believe in gravity?",
                pub_date=timezone.now()
            )
        response = self.client.get(reverse('polls:vote', args=(question.id,)))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_vote(self):
        self.client.login(username="Mag", password="jotaro")
        question = Question.objects.create(
                question_text="Do you believe in gravity?",
                pub_date=timezone.now()
            )
        response = self.client.get(reverse('polls:vote', args=(question.id,)))
        self.assertEqual(response.status_code, 200)