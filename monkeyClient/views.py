from django.shortcuts import render,render_to_response
from monkeyClient.forms import basicInfo,addMonkey,metasploitDBInfo
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
import smclient
from helperFunctions import openMDB
from monkeyClient.models import monkeyDBInfo,metasploitInfo
from pymongo import MongoClient

# Create your views here.

def basicInfoForm(request):
	if request.method == 'POST':
		if 'submit_Monkey' in request.POST:
			form = basicInfo(request.POST,request.FILES)
		else:
			form = metasploitDBInfo(request.POST)
		if form.is_valid() and 'submit_Monkey' in request.POST:
			cd=form.cleaned_data
			options={}
			options['dbip'] = cd['IP']
			options['dbname'] = cd['Name']
			options['eraseTargetsData']=str(cd["targetErase"]).lower()
			options['CLI']='false'
			db=openMDB(options['dbip'],options['dbname'])
			

			if 'file' in request.FILES and db is not None:
				smclient.loadTargetsParam(options,request.FILES['file'],db)
			form.save()
			return HttpResponseRedirect('/client')
		elif form.is_valid() and 'submit_Metasploit' in request.POST:
			cd=form.cleaned_data
			options={}
			options['CLI']='false'
			dbConfig=monkeyDBInfo.objects.get()
			options['dbip']=dbConfig.IP
			options['dbname']=dbConfig.Name
			options['eraseSploitData']=str(cd['metErase']).lower()
			smclient.dbLoadModules(options,cd['IP'],cd['username'],cd['password'],cd['Name'])
			form.save()
			return HttpResponseRedirect('/client')
		else:
			print form.errors
			return HttpResponseRedirect('/client?e=1')

		#dostuff
#insert redirect
		#return HttpResponseRedirect('/client')
	else:
			
		try:
			form=basicInfo(instance=monkeyDBInfo.objects.get())
		except monkeyDBInfo.DoesNotExist:
			form=basicInfo()
		try:
			metaForm=metasploitDBInfo(instance=metasploitInfo.objects.get())
		except metasploitInfo.DoesNotExist:
			metaForm=metasploitDBInfo()	
	args={}
	args.update(csrf(request))
	args['form']=form
	args['metaForm']=metaForm
	if(request.GET.get('e')):
		args['error']=request.GET.get('e')
	return render_to_response('client.html',args)

def monkeyForm(request):
	if request.method =='POST':
		form = addMonkey(request.POST)
		if form.is_valid():
			cd=form.cleaned_data
			options={}
			options['CLI']='false'
			options['eraseMonkeyData']='false'
			try:
				dbInfo=monkeyDBInfo.objects.get()
				options['dbip']=dbInfo.IP
				options['dbname']=dbInfo.Name
				db=openMDB(options['dbip'],options['dbname'])
				if db is not None:
					smclient.loadMonkeys(options,db,[int(cd['iq'])],[int(cd['type'])],[cd['loc']],[cd['ip']],[cd['minbytes']],[cd['maxbytes']])
			except monkeyDBInfo.DoesNotExist:
				#error
				print 'monkey db info does not exist'
		return HttpResponseRedirect('/monkeys')
	else:
		if(request.GET.get('btnStart')):
			options=getDBOptions()
			db=openMDB(options['dbip'],options['dbname'])
			options['runTime']=request.GET.get('duration')
			if db is not None:
				smclient.startMonkeysParam(options,db)
		form=addMonkey()
	return render(request,'monkeys.html',{'form':form})

def resultsForm(request):
	if request.method =='POST':
		
		return HttpResponseRedirect('/results')
	else:
		options=getDBOptions()
		db=openMDB(options['dbip'],options['dbname'])
		if db is not None:
			actions={}
			columnOrder=['action','monkeyIP','targetIP','port','start','end','bytes']
			columns={'action':'Action Taken','targetIP':'Target IP','port':'Port','monkeyIP':'Monkey IP','start':'Start Time','end':'End Time','bytes':'Bytes Sent'}
			count=0
                	for event in db.actions.find():
				monkey=db.monkeys.find_one({'id' : event['id']})
				action={}
				action['action']=event['action']
				action['monkeyIP']=str(monkey['ip'])
				action['targetIP']=event['ip']
				action['start']=event['start']
				action['end']=event['end']
				if event['action']=='fuzz':
					action['port']=event['port']
					action['bytes']=event['bytes']
				elif event['action']=='synscan':
					action['port']='N/A'
					action['bytes']='N/A'
				else:
					action['port']=event['port']
					action['bytes']='N/A'
				actions[count]=action
				count=count+1

	
			return render_to_response('results.html', {'actions': actions,'columns':columns,'order':columnOrder})
		else:
			return render_to_response('results.html')

def getDBOptions():
	try:
		dbInfo=monkeyDBInfo.objects.get()
		options={}
		options['dbip']=dbInfo.IP
		options['dbname']=dbInfo.Name
		return options
	except monkeyDBInfo.DoesNotExist:
		print 'monkey db info does not exist'
		return NULL
