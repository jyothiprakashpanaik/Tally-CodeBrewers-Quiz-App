

from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index_view"),
    path("<str:username>/<int:quiz_id>", views.start_quiz, name="start_quiz_view"),
    path("submit_answer/<int:quiz_id>/<int:question_id>", views.submit_answer, name="submit_answer_view"),
    path("email_auth", views.email_auth, name="email_auth_view"),
    path("<int:quiz_id>/results",views.results, name="results_view"),
]
