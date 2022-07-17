from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q,Sum, Count, Min, Max, Avg
from .models import QuizName,QuizQuestion,QuizAnswer,QuizResponces
from django.contrib import messages

from datetime import datetime, timezone
import os
import math

@login_required(redirect_field_name='login')
def home(request):
	print("home")

	user = request.user

	# user = User.objects.filter(Q(is_staff=True) & Q(username=user.username))

	quizzes = QuizName.objects.filter(created_by=user)

	quiz_details = []

	for quiz in quizzes:
		quiz_details.append(
		{
		"title":quiz.title,
		"id":quiz.id,
		"description":quiz.description,
		"update": math.floor((datetime.now(timezone.utc) - quiz.updated_at).total_seconds()/60),
		"image":quiz.image
		})

	context={"user":user.username,"quiz_details":quiz_details}
		

	return render(request, "main/home.html",context=context)
	
current_quize = None

@login_required(redirect_field_name='login')
def new_quiz(request):
	print("Create a New Quize")
	if request.method=="POST":
		quiz_name = request.POST['inputTitle']
		quiz_icon = request.POST.get('inputImage',None)
		quiz_decs = request.POST.get('inputDescription', None)



		if QuizName.objects.filter(Q(title=quiz_name) & Q(created_by=request.user)).exists():
			messages.info(request, "Quiz Name already exists")
			return redirect("/quizadmin/new_quiz")


		quiz = QuizName.objects.create(created_by=request.user, title=quiz_name)

		# if quiz_decs and quiz_icon:
		# 	# quiz.save()
		# elif quiz_decs:
		# 	quiz = QuizName.objects.create(created_by=request.user, title=quiz_name, description=quiz_decs)
		# 	# quiz.save()
		# elif quiz_icon:
		# 	quiz = QuizName.objects.create(created_by=request.user, title=quiz_name, description=quiz_decs, image=quiz_icon)
		# 	# quiz.save()

		quiz.save()
		messages.success(request, "Quiz Created")
		
		return redirect(f"/quizadmin/{quiz.id}/add_questions")
	return render(request, "main/new_quiz.html")


@login_required(redirect_field_name='login')
def add_questions(request, qid):
	print("Add Questions")
	quiz = QuizName.objects.get(id=qid)

	if request.user!=quiz.created_by:
		return redirect("/")

	if request.method=="POST":
		keys = list(request.POST.keys())
		options_list = []
		for key in keys:
			if "option" in key and key!="correct_options":
				options_list.append(key)

		question = request.POST["question"]
		marks = request.POST["marks"]


		correct_options = request.POST.getlist("correct_options")

		question = QuizQuestion.objects.create(quiz_name=quiz,quiz_question=question,marks=marks)
		question.save()

		for option in options_list:
			print((option, correct_options))
			answer = QuizAnswer.objects.create(question=question,answer=request.POST[option],is_correct=(option in correct_options))
			answer.save()

		return redirect(f"/quizadmin/{qid}/add_questions")

	questions = QuizQuestion.objects.filter(quiz_name=quiz).all()

	questionbank_list = []
	for que in questions:
		questionbank_list.append({
			"question": que.quiz_question,
			"question_id": que.id,
			"marks": que.marks,
			"options": que.answer_options,
		})

	context = {"questions":questionbank_list,"correct":"true"}

	return render(request, "main/add_questions.html", context=context)


@login_required(redirect_field_name='login')
def stats(request, qid):

	quiz = QuizName.objects.get(id=qid)
	questions = QuizQuestion.objects.filter(quiz_name=quiz).all()
	quiz_responce = QuizResponces.objects.filter(attempt_quiz=quiz)

	questions_details = []
	mx=0
	for question in questions:
		qr = quiz_responce.filter(user_question=question).values("user_email")
		questions_details.append({
			"question": question.quiz_question,
			"question_marks": question.marks,
			"total_attempts": qr.distinct().count(),
			"total_correct_attempts": qr.filter(marks__lte=0)
			})
	
	total_number_of_questions = len(questions)
	total_marks = questions.aggregate(Sum('marks'))['marks__sum']
	total_quiz_attend = quiz_responce.values('user_email').distinct().count()



	quiz_responce =  quiz_responce.values('user_email').order_by('user_email').annotate(Sum('marks')).values_list('marks__sum')
	

	max_score = quiz_responce.aggregate(Max('marks__sum'))
	min_score = quiz_responce.aggregate(Min('marks__sum'))
	average_score = quiz_responce.aggregate(Avg('marks__sum'))


	context = {"questions_details": questions_details, "min_score": min_score,"max_score": max_score, 
	"average_score":average_score,"total_number_of_questions":total_number_of_questions,"total_marks":total_marks,"total_quiz_attend":total_quiz_attend}
	return render(request, "main/stats.html", context=context)

