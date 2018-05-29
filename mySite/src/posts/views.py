from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
import datetime

# Create your views here.
from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from .models import Post


def post_create(request):
	if not request.user.is_active or not request.user.is_staff:
		raise Http404

	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request, "Sucessfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"form" : form,
	}
	return render(request, "post_form.html", context)

def post_content(request, slug):
	instance = get_object_or_404(Post, slug=slug)
	if instance.draft:
		if not request.user.is_active or not request.user.is_staff:
			raise Http404

	initial_data = {
		"content_type" : instance.get_content_type,
		"object_id" : instance.id
	}
	
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()

		new_comment, created = Comment.objects.get_or_create(
								user = request.user,
								content_type = content_type,
								object_id = obj_id,
								content = content_data,
								parent = parent_obj,
							)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments

	context = {
		"title" : instance.title,
		"instance" : instance,
		"comments" : comments,
		"comment_form" : form,
	}
	return render(request, "post_content.html", context)

def post_list(request):
	if request.user.is_active or request.user.is_staff:
		title = "Post List"
	else:
		title = "Discover"

	from_date1 = datetime.datetime.now() - datetime.timedelta(days=1)
	from_date2 = datetime.datetime.now() - datetime.timedelta(days=7)

	queryset_list_day = Post.objects.active().order_by("-timestamp").filter(
					timestamp__range=[from_date1, datetime.datetime.now()]
				)

	queryset_list_week = Post.objects.active().order_by("-timestamp").filter(
					timestamp__range=[from_date2, datetime.datetime.now()]
				)

	queryset_list_older = Post.objects.active().order_by("-timestamp")

	query = request.GET.get('q')
	if query:
		queryset_list_day = queryset_list_day.filter(
			Q(title__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct().order_by("-timestamp")

		queryset_list_week = queryset_list_week.filter(
			Q(title__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct().order_by("-timestamp")

		queryset_list_older = queryset_list_older.filter(
			Q(title__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct().order_by("-timestamp")

	paginator1 = Paginator(queryset_list_day, 6)
	paginator2 = Paginator(queryset_list_week, 6)
	paginator3 = Paginator(queryset_list_older, 6)

	page_request_var = "page"
	page = request.GET.get(page_request_var)
	
	try:
		queryset1 = paginator1.page(page)
	except PageNotAnInteger:
		queryset1 = paginator1.page(1)
	except EmptyPage:
		queryset1 = paginator1.page(paginator1.num_pages)

	try:
		queryset2 = paginator2.page(page)
	except PageNotAnInteger:
		queryset2 = paginator2.page(1)
	except EmptyPage:
		queryset2 = paginator2.page(paginator2.num_pages)
		
	try:
		queryset3 = paginator3.page(page)
	except PageNotAnInteger:
		queryset3 = paginator3.page(1)
	except EmptyPage:
		queryset3 = paginator3.page(paginator3.num_pages)

	context = {
		"object_list_day" : queryset1,
		"object_list_week" : queryset2,
		"object_list_older" : queryset3,
		"title" : title,
		"page_request_var" : page_request_var,
	}
	if request.user.is_active or request.user.is_staff:
		return render(request, "post_list.html", context)
	else:	
		return render(request, "discover.html", context)

def post_update(request, slug=None):
	if not request.user.is_active or not request.user.is_staff:
		raise Http404

	instance = get_object_or_404(Post, slug=slug)
	if not instance.user == request.user:
		raise Http404
		
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request, "Sucessfully Updated")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"title" : instance.title,
		"instance" : instance,
		"form" : form,
	}
	return render(request, "post_form.html", context)

def post_delete(request, slug=None):
	if not request.user.is_active or not request.user.is_staff:
		raise Http404

	instance = get_object_or_404(Post, slug=slug)
	if not instance.user == request.user:
		raise Http404

	instance.delete()
	messages.success(request, "Sucessfully Deleted")
	return redirect("posts:list")
