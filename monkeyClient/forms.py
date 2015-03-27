from django import forms
from models import monkeyDBInfo

class basicInfo(forms.ModelForm):
	IP=forms.CharField(label='Database IP')
	Name=forms.CharField(label="Database Name")
	file=forms.FileField(label="Upload Targets",required=False)
	targetErase=forms.BooleanField(label="Erase Existing Targets",required=False)
	class Meta:
		model=monkeyDBInfo
class addMonkey(forms.Form):
	iqList=(("0","0-World\'s #1 Hacker"),("1",'1-CISSP'),("2",'2-CEH'),("3",'3-Security Weekly Listener'))
	iq=forms.ChoiceField(choices=iqList,label="Monkey IQ")
	typeList=(("1",'Scanner Monkey'),("2",'Exploit Monkey'),("3",'Fuzzy Monkey'),("4",'Login Monkey'),("5",'Web Monkey'))
	type=forms.ChoiceField(choices=typeList, label="Monkey Type")
	locList=(('i','Internal'),('e','External'))
	loc=forms.ChoiceField(choices=locList,label="Monkey Location")
	ip=forms.CharField(max_length=16,label='Monkey Server IP')
