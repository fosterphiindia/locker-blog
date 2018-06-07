from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from .forms import UserRegisterForm
from .models import Account

def save_profile(backend, user, response, *args, **kwargs):
	print(response)
	if backend.name == "facebook":
		if not Account.objects.filter(user=user).exists():
			Account.objects.create(
					user = user,
					title = "ABC",
					first_name = response['name'],
					last_name = response['name'],
					email = response['email'],
					location = 'qwerty'
					# location = response['user_location']
					)
	if backend.name == "twitter":		
		if not Account.objects.filter(user=user).exists():
			Account.objects.create(
					user = user,
					title = "ABC",
					first_name = response['name'],
					last_name = response['name'],
					email = 'nis@nis.com',
					location = response['location']
					)

	if backend.name == "google-oauth2":		
		if not Account.objects.filter(user=user).exists():
			Account.objects.create(
					user = user,
					title = "ABC",
					first_name = response['name']['givenName'],
					last_name = response['name']['familyName'],
					email = response['emails'][0]['value'],
					location = 'qwerty'
					# location = response['location']
					)

	User = get_user_model()
	user = User.objects.get(username=user)
	user.is_staff = True
	user.save()
	group = Group.objects.get(name='registered_users')
	user.groups.add(group)