from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
import datetime

# Create your models here.


def upload_location(instance, filename):
	now = datetime.datetime.now()
	return "%s/%s/%s/%s/%s" %(instance.user, now.year, now.month, now.day, filename)

class Account(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=120, null=True, blank=True)
	first_name = models.CharField(max_length=120, null=True, blank=True)
	last_name = models.CharField(max_length=120, null=True, blank=True)
	email = models.CharField(max_length=120, null=True, blank=True)
	location = models.CharField(max_length=120, null=True, blank=True)
	token = models.CharField(max_length=320, null=True, blank=True)
	image = models.ImageField(upload_to=upload_location,
		null=True,
		blank=True,
		height_field="height_field",
		width_field="width_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)

	# objects = PostManager()

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

	# def get_absolute_url(self):
		# return reverse("accounts", kwargs={"user" : self.id})

	class Meta:
		ordering = ["user"]

	# @property
	# def comments(self):
	# 	instance = self
	# 	qs = Comment.objects.filter_by_instance(instance)
	# 	return qs

	# @property
	# def get_content_type(self):
	# 	instance = self
	# 	content_type = ContentType.objects.get_for_model(instance.__class__)
	# 	return content_type

