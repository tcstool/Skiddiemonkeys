from django.conf.urls import patterns, url

from monkeyClient import views

urlpatterns = patterns('',
	url(r'client/$', views.basicInfoForm, name='basicInfoForm'),
	url(r'monkeys/',views.monkeyForm, name='monkeyForm'),
	url(r'results/',views.resultsForm, name='resultsForm'),
)
