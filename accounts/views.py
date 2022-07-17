from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

def login(request):
	if request.method=="POST":
		username = request.POST["username"]
		password = request.POST["password"]

		user = auth.authenticate(username=username, password=password)
		
		print(user)

		if user is not None:
			auth.login(request, user)
				
			if user.is_staff:
				return redirect("/quizadmin")

			return redirect("/")
		else:
			messages.info(request, "No user found")
			return redirect("/accounts/login")

	return render(request, "accounts/login.html")

def logout(request):
	auth.logout(request)
	print("user logedout")
	return redirect("/")

def register(request):
	if request.method=="POST":
		first_name = request.POST["first_name"]
		last_name = request.POST["last_name"]
		username = request.POST["username"]
		email = request.POST["email"]
		account_type = True if request.POST["account_type"]=="QuizzAdmin" else False

		password = request.POST["password"]
		password2 = request.POST["password2"]

		if User.objects.filter(username=username).exists():
			print("Username alredy taken")
			messages.info(request, 'Username alredy taken.')
			return redirect("/accounts/register")

		if User.objects.filter(email=email).exists():
			print("Email alredy exists")
			messages.info(request, 'Email alredy exists.')
			return redirect("/accounts/register")

		if password!=password2:
			print("password not matching...")
			messages.info(request, 'Password not matching.')
			return redirect("/accounts/register")

		user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,is_staff=account_type,password=password)
		user.save()

		return redirect("/accounts/login")


	return render(request, "accounts/register.html")