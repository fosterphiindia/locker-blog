from pagedown.widgets import PagedownWidget
from django import forms
from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout
	)

from .models import Account

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This user does not exists")

			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")

			if not user.is_active:
				raise forms.ValidationError("This user is no longer active")

		return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label="Email Address")
	email2 = forms.EmailField(label="Confirm Email")
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = [
			"first_name",
			"last_name",
			"username",
			"email",
			"email2",
			"password",
		]

	def clean(self, *args, **kwargs):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError("Emails must match")

		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered")

		return super(UserRegisterForm, self).clean(*args, **kwargs)

	# def clean_email2(self):
	# 	email = self.cleaned_data.get('email')
	# 	email2 = self.cleaned_data.get('email2')
	# 	if email != email2:
	# 		raise forms.ValidationError("Emails must match")

	# 	email_qs = User.objects.filter(email=email)
	# 	if email_qs.exists():
	# 		raise forms.ValidationError("This email has already been registered")
			
	# 	return email


class EditProfileForm(forms.ModelForm):
	# title = forms.CharField(widget=forms.HiddenInput)
	# first_name = forms.CharField(widget=forms.HiddenInput)
	# last_name = forms.CharField(widget=forms.HiddenInput)
	# location = forms.CharField(widget=forms.HiddenInput)
	# email = forms.CharField(widget=forms.HiddenInput)
	# image = forms.ImageField(widget=forms.HiddenInput)
	class Meta:
		model = Account
		fields = [
			"title",
			"first_name",
			"last_name",
			"image",
			"email",
			"location",
		]