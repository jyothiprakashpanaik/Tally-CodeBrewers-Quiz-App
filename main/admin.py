from django.contrib import admin
from .models import QuizName, QuizQuestion, QuizAnswer, QuizResponces

admin.site.register(QuizName)


class QuizAnswerAdmin(admin.StackedInline):
	model = QuizAnswer

class QuizQuestionAdmin(admin.ModelAdmin):
	inlines = [QuizAnswerAdmin]

admin.site.register(QuizQuestion, QuizQuestionAdmin)


admin.site.register(QuizAnswer)

class QuizResponcesAdmin(admin.ModelAdmin):
	model = QuizResponces
	list_display = ["user_email","user_question","marks"]

admin.site.register(QuizResponces, QuizResponcesAdmin)