from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home_view"),
    path("new_quiz", views.new_quiz, name="new_quiz_view"),
    path("<str:qid>/add_questions", views.add_questions, name="add_questions_view"),
    path("<str:qid>/stats", views.stats, name="stats_view"),
]
