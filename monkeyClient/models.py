from django.db import models
from solo.models import SingletonModel

class monkeyDBInfo(SingletonModel):
	IP=models.CharField(max_length=25)
	Name=models.CharField(max_length=50)

	def __unicode__(self):
		return u"Monkey DB Info"

class metasploitInfo(SingletonModel):
	IP=models.CharField(max_length=25)
	username=models.CharField(max_length=50)
	password=models.CharField(max_length=50)
	Name=models.CharField(max_length=50)

	def __unicode__(self):
		return u"Monkey Metasploit DB Info"

class targetFile(models.Model):
	fileName=models.CharField(max_length=200)

class monkey(models.Model):
	IQ=models.IntegerField(default=0)
	Type=models.IntegerField(default=1)
	Location=models.CharField(max_length=1)
	ServerIP=models.CharField(max_length=25)
	MinFuzz=models.IntegerField(default=1)
	MaxFuzz=models.IntegerField(default=1)
# Create your models here.
