from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from .validators import validate_file_extension
import datetime
# Create your models here.

from comments.models import Comment


class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(PostManager, self).filter(draft=False)

def upload_location(instance, filename):
	now = datetime.datetime.now()
	return "%s/%s/%s/%s/%s" %(instance.user, now.year, now.month, now.day, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to=upload_location,
		null=True,
		blank=True,
		height_field="height_field",
		width_field="width_field")
	# video = models.FileField(upload_to = upload_location, null=True, blank=True,)
	video = models.FileField(
				upload_to=upload_location,
				validators=[validate_file_extension],
				null=True,
				blank=True,
			)
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	draft = models.BooleanField(default=False)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	objects = PostManager()

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:content", kwargs={"slug" : self.slug})

	class Meta:
		ordering = ["-timestamp", "-updated"]

	@property
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(instance)
		return qs

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type


def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")	
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_reciever, sender=Post)