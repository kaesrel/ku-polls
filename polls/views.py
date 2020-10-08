from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import Choice, Question


class IndexView(generic.ListView):
    """View of the index page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()
                                       ).order_by('-pub_date')
        # return Question.objects.all()


class DetailView(generic.DetailView):
    """View of the detail page."""

    model = Question
    template_name = 'polls/detail.html'

    # def get_queryset(self):
    #     return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """Handle request and return the appropriate response page."""
        try:
            question = Question.objects.get(pk=kwargs['pk'])
            if not question.can_vote():
                messages.error(request, "That question is not allowed for voting.")
                return redirect('polls:index')
        except ObjectDoesNotExist:
            messages.error(request, "That question does not exist.")
            return redirect('polls:index')
        # try:
        #     self.object = self.get_object()
        # except Http404:
        #     # messages.error(request, "That question is not allowed for voting.")
        #     messages.error(request, kwargs['pk'])
        #     return redirect('polls:index')
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ResultsView(generic.DetailView):
    """View of the result page."""

    model = Question
    template_name = 'polls/results.html'

    def get(self, request, *args, **kwargs):
        """Handle request and return the appropriate response page."""
        try:
            question = Question.objects.get(pk=kwargs['pk'])
            if not question.is_published():
                messages.error(request, "That question is not published yet.")
                return redirect('polls:index')
        except ObjectDoesNotExist:
            messages.error(request, "That question does not exist.")
            return redirect('polls:index')
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


def vote(request, question_id):
    """Handle the vote request and return an appropriate response."""
    question = get_object_or_404(Question, pk=question_id)
    # if not question.can_vote():
    #     # messages.error(request, "This question is not allowed for voting.")
    #     # return redirect('polls:index')
    #     return HttpResponseRedirect(reverse('polls:index'),
    #     messages.error(request, "This question is not allowed for voting."))
    try:
        selected_choice = \
            question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',
                      {
                          'question': question,
                          'error_message': "You didn't select a choice.",
                      })
    else:  # other exceptions or succession
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse(
            'polls:results',
            args=(question.id,)
        ))
