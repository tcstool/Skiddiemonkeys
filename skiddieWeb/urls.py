from django.conf.urls import patterns, include, url
from django.contrib import admin
from monkeyClient import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'skiddieWeb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^client/$', views.basicInfoForm, name='basicInfoForm'),
    url(r'^monkeys/$', views.monkeyForm, name='monkeyForm'), 
    url(r'^results/$', views.resultsForm, name='resultsForm'),
)
