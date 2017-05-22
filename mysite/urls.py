from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from mysite.core import views as core_views
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls,)),
    url(r'^my/$', core_views.home, name='home'),
    url(r'^my/categories', core_views.addCategory, name='category'),
    url(r'^my/add', core_views.add, name='add'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
]
