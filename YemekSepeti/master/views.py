from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm


def index(request):
	return render(request, 'index.html')

def profile(request):
	return render(request, 'profile.html')

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.register()
			auth_login(request, user)
			return redirect('master:index')
		else:
			print(form.errors)
	return render(request, 'register.html')

def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid() and form.login(request):
			return redirect('master:index')
	return render(request, 'login.html')

@login_required
def logout(request):
	auth_logout(request)
	return redirect('master:index')