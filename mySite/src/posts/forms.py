from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post


class PostForm(forms.ModelForm):
	content = forms.CharField(widget=PagedownWidget)
	# video = forms.FileField(widget=forms.FileInput(attrs={'accept': '.mp4,video/quicktime'}))
	class Meta:
		model = Post
		fields = [
			"title",
			"image",
			"video",
			"content",
			"draft",
		]