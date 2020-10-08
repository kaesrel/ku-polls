"""Collection of views of mysite project."""
from django.shortcuts import redirect

def index(request):
    """Return the redirection to index page."""
    return redirect("polls:index")


# from polls.views import IndexView
# path('', IndexView.as_view(), name="main_index")
# path('', views.index, name="main_index"),
