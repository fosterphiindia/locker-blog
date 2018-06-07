from django.conf import settings
from django.contrib import messages
from django.middleware import csrf
from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout
	)
from django.core.paginator import Paginator, PageNotAnInteger
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group

# Create your views here.
from .forms import UserLoginForm, UserRegisterForm, EditProfileForm
from posts.models import Post
from .models import Account


def login_view(request):
	print(request.user.is_authenticated())
	next = request.GET.get('next')
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request, user)
		if next:
			return redirect(next)
		return redirect("/posts/")

	return render(request, "form.html", {"form":form, "title":title})

def logout_view(request):
	logout(request)
	return redirect("/posts/")

def save_user(request):
	form = EditProfileForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.title = "ABC"
		instance.first_name = request.user.first_name
		instance.last_name = request.user.last_name
		instance.email = request.user.email
		instance.location = "asd"
		csrf.get_token(request)
		instance.save()

	return render(request, "form.html", {"form":form})

def register_view(request):
	print(request.user.is_authenticated())
	next = request.GET.get('next')
	title = "Register"
	form = UserRegisterForm(request.POST or None)

	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.is_staff = True
		user.save()
		group = Group.objects.get(name='registered_users')
		user.groups.add(group)

		subject = 'Test Subject'
		message = 'Test Message'
		from_email = settings.EMAIL_HOST_USER
		to_list = [user.email]

		send_mail(subject, message, from_email, to_list, fail_silently=True)

		
		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)
		save_user(request)

		if next:
			return redirect(next)
		return redirect("/posts/")

	context = {
		"form" : form,
		"title" : title,
	}

	return render(request, "form.html", context)


def view_profile(request):
	queryset_list = Post.objects.active().order_by("-timestamp").filter(user=request.user)
	query = request.GET.get('q')
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct().order_by("-timestamp")

	paginator = Paginator(queryset_list, 6)
	page_request_var = "page"
	page = request.GET.get(page_request_var)

	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	title = "User Profile"
	context = {
		"title" : title,
		"object_list" : queryset,
	}
	return render(request, "view_profile.html", context)


def edit_profile(request, user=None):
	# if not request.user.is_active or not request.user.is_staff:
	# 	raise Http404

	instance = get_object_or_404(Account, user=request.user)
	# if not instance.user == request.user:
	# 	raise Http404

	form = EditProfileForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request, "Sucessfully Created")
		return HttpResponseRedirect(view_profile)

	title = "User Profile"
	context = {
		"title" : title,
		"form" : form,
	}

	return render(request, "edit_profile.html", context)

def forget_password(email):
	if Account.objects.filter(email=email).exists():
		Account.objects.update(token='some_value')

	return redirect("/posts/")

def reset_password(request, user=None):
	instance = get_object_or_404(Account, user=request.user)	