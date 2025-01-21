from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from .models import User

class LoginForm(forms.Form):
	username = forms.CharField(max_length=255, required=True)
	password = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput)

	def login(self, request):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(request, username=username, password=password)

		if user is not None and user.is_active:
			login(request, user)
			return True
		return False


class RegisterForm(UserCreationForm):
	email = forms.EmailField(max_length=255, required=True)

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

	def register(self, commit=True):
		# Save the user (basic)
		user = super().save(commit=False)
		user.email = self.cleaned_data.get('email')
		

		if commit:
			user.save()

		return user
