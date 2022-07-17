from django.shortcuts import render, HttpResponse, redirect
from main.models import QuizQuestion, QuizAnswer, QuizName, QuizResponces
from django.http import JsonResponse
import random
from django.contrib import messages

from django.db.models import Q



def index(request):
	total_quiz_attend = 0
	quiz_list = []
	

	if request.user.is_authenticated:
		quiz_responses = QuizResponces.objects.filter(user_email=request.user.email).values("attempt_quiz").distinct()
		total_quiz_attend = len(quiz_responses)

	context = {
	"total_quiz_attend": total_quiz_attend
	}

	return render(request, "home/index.html", context=context)


def results(request,quiz_id):

	try:
		email = ""
		username=""
		score = 0
		if request.user.is_authenticated:
			email = request.user.email
			username = request.user.username
		else:
			email = request.session["email"]
			username = "AnonymousUser"



		quiz = QuizName.objects.get(id=quiz_id)
		questions = QuizQuestion.objects.filter(quiz_name=quiz).all()
		

		questions_report = []

		for question in questions:
			marks = QuizResponces.objects.get(Q(user_email=email) & Q(user_question=question)).marks
			questions_report.append({
				"question": question.quiz_question,
				"correct_options": question.answer_options(),
				"marks_awarded": marks, 
				"question_marks": question.marks,
			})
			score+=marks

		context = {"score": score, "email": email, "username":username, "quiz_name": quiz.title, "questions_report": questions_report}

		return render(request, "home/result.html",context=context)

	except Exception as e:
		print(e)
		return HttpResponse("Error plz try again.!")

def submit_answer(request, quiz_id, question_id):

	if request.method=="POST":
		quiz = QuizName.objects.get(id=quiz_id)
		user_email = request.session["email"]
		user_options = [i.replace("option","") for i in request.POST if "option" in i]
		user_question = QuizQuestion.objects.get(id=question_id)
		corrects_answers = user_question.correct_answers()
		score = 0

		for user_option in user_options:
			if user_option not in corrects_answers:
				break
		else:
			if len(user_options)==len(corrects_answers):
				score+=user_question.marks
			else:
				score = 0

		if(QuizResponces.objects.filter(user_email=user_email,user_question=user_question).exists()):
			messages.warning(request, "You cant change Your response of already submitted question")
		else:
			quiz_responce = QuizResponces.objects.create(user_email=user_email,attempt_quiz=quiz,user_question=user_question,marks=score)
			quiz_responce.save()

		exclude_questions = QuizResponces.objects.filter(user_email=user_email).values_list("user_question_id",flat=True)
		question = QuizQuestion.objects.filter(quiz_name=quiz).exclude(id__in=exclude_questions).first()

		print(question)


		if question:
			context = {"quiz_title":quiz.title,"quiz_id":quiz.id,"question_id":question.id,"question": {
				"question": question.quiz_question,
				"marks": question.marks,
				"options": question.answer_options(),
				"timer": question.timer
			}}

			
			messages.success(request, "Your Response save it cant be changed.")

			return render(request, "home/quiz.html", context=context)

		else:
			messages.success(request, "Quiz submitted!.")

			return redirect(f"/{quiz_id}/results")
	else:
		messages.warning(request, "Access Denial! Please verify your email for further proceedings.")
		messages.info(request, "If you have submitted any question, it is stored in the server you can resume your test.")
		return render(request, "home/email_auth.html")


def email_auth(request):
	messages.warning(request, "Please provide your email Id")

	if request.user.is_authenticated:
		request.session["email"] = request.user.email
		(username, quiz_id)=request.session["test_page"]
		return redirect(f"/{username}/{quiz_id}")

	if request.method=="POST":
		request.session["email"] = request.POST["email"]
		(username, quiz_id)=request.session["test_page"]
		return redirect(f"/{username}/{quiz_id}")

	return render(request, "home/email_auth.html")

def start_quiz(request,username,quiz_id):

	if request.user.is_anonymous and request.session.get("email","")=="":
		request.session["test_page"] = (username, quiz_id)
		return redirect("email_auth_view")
	elif request.user.is_authenticated:
		request.session["email"] = request.user.email

	if len(QuizResponces.objects.filter(user_email=request.session["email"], attempt_quiz__id=quiz_id).all()) >= len(QuizQuestion.objects.filter(quiz_name__id=quiz_id)):
		messages.info(request,"Your response is stored can not reattempt the same quiz." )
		return redirect("/")

	print(request.session["email"])

	try:
		quiz = QuizName.objects.get(id=quiz_id)
		question = QuizQuestion.objects.filter(quiz_name=quiz).first()
		
		context = {"quiz_title":quiz.title,"quiz_id":quiz.id,"question_id":question.id,"question": {
				"question": question.quiz_question,
				"marks": question.marks,
				"options": question.answer_options(),
				"timer": question.timer
		}}

		return render(request, "home/quiz.html", context=context)

	except Exception as e:
		print(e)

	return HttpResponse("Error",404)