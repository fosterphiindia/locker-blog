"""mySite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from accounts.views import (login_view, register_view, logout_view,
                            view_profile, edit_profile, save_user,
                            forget_password)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include("posts.urls", namespace="posts")),
    url(r'^comments/', include("comments.urls", namespace="comments")),
    url(r'^register/', register_view, name="register"),
    url(r'^login/', login_view, name="login"),
    url(r'^logout/', logout_view, name="logout"),
    url(r'^oauth/', include('social_django.urls', namespace='social')), 
    url(r'^profile/', view_profile, name="profile"),
    url(r'^edit-profile/', edit_profile, name="edit_profile"),
    url(r'^save-user/', save_user, name="save_user"),
    url(r'^forget-password/', forget_password, name="forget_password"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)