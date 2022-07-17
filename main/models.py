from django.db import models
from django.contrib.auth.models import User
import random

class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta(object):
		abstract=True


class QuizName(BaseModel):
	created_by = models.ForeignKey(User, related_name='quiz_created_by',on_delete=models.CASCADE)
	title = models.CharField(max_length=100, null=False, blank=False)
	description = models.TextField(default="this quiz was created on quizzApp")
	image = models.ImageField(upload_to="static/media/quiz_icon", default="quiz_icon/default.jpg")
	
	class Meta:
		ordering = ['title']
		unique_together = ['title', 'created_by']

	def __str__(self):
		return self.title

class QuizQuestion(BaseModel):
	quiz_name = models.ForeignKey(QuizName, related_name='quiz_name', on_delete=models.CASCADE)
	quiz_question = models.TextField(null=False, blank=False)
	marks = models.IntegerField(default=0)

	timer = models.IntegerField(default=1)

	def __str__(self):
		return self.quiz_question

	def answer_options(self):
		options = []
		for quizanswer in QuizAnswer.objects.filter(question=self).all():
			options.append({
				"answer": quizanswer.answer,
				"correct": quizanswer.is_correct,
				"id": quizanswer.id  
				})
		return options

	def correct_answers(self):
		corrects = []
		for quizanswer in QuizAnswer.objects.filter(question=self).all():
			if quizanswer.is_correct:
				corrects.append(str(quizanswer.id))
		return corrects

class QuizAnswer(BaseModel):
	question = models.ForeignKey(QuizQuestion, related_name='question', on_delete=models.CASCADE)
	answer = models.TextField(null=False, blank=False)
	is_correct = models.BooleanField(default=False)

	def __str__(self):
		return self.answer


class QuizResponces(BaseModel):
	user_email = models.EmailField(max_length=50, null=False,blank=False)
	user_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="user_question_answer")
	attempt_quiz = models.ForeignKey(QuizName, on_delete=models.CASCADE, related_name="attempt_quiz", default=None)

	marks = models.IntegerField(default=0)

	

	class Meta:
		unique_together = ["user_email","user_question"]

	def __str__(self):
		return self.user_email + " " + str(self.user_question.id)

