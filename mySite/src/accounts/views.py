from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout
	)
from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group

# Create your views here.
from .forms import UserLoginForm, UserRegisterForm
from posts.models import Post



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

def register_view(request):
	print(request.user.is_authenticated())
	next = request.GET.get('next')
	title = "Register"
	form = UserRegisterForm(request.POST or None)

	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.is_staff = True
		user.set_password(password)
		user.save()
		group = Group.objects.get(name='registered_users')
		user.groups.add(group)
		# user.groups.add(Group.objects.get(name='registered_users'))
		# user = kwargs["instance"]
	# if kwargs["created"]:

		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)

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


def edit_profile(request):
	# queryset_list = Post.objects.active().order_by("-timestamp").filter(user=request.user)
	# query = request.GET.get('q')
	# if query:
	# 	queryset_list = queryset_list.filter(
	# 		Q(title__icontains=query)|
	# 		Q(user__first_name__icontains=query)|
	# 		Q(user__last_name__icontains=query)
	# 		).distinct().order_by("-timestamp")

	# paginator = Paginator(queryset_list, 6)
	# page_request_var = "page"
	# page = request.GET.get(page_request_var)

	# try:
	# 	queryset = paginator.page(page)
	# except PageNotAnInteger:
	# 	queryset = paginator.page(1)
	# except EmptyPage:
	# 	queryset = paginator.page(paginator.num_pages)

	# title = "User Profile"
	# context = {
	# 	"title" : title,
	# 	"object_list" : queryset,
	# }
	return render(request, "edit_profile.html", {})