from django.template.defaulttags import register

@register.filter
def get_key(dictionary,orderA):
	res=""
	for key in orderA:
		res+="<th>"+dictionary[key]+"</th>"
	return res

@register.filter
def get_actions(actions,orderA):
	res=""
	for act in actions:
		res+="<tr>"
		for col in orderA:
			ac=actions[act]
			ca=ac[col]
			res+="<td>"+str(ac[col])+"</td>"
		res+="</tr>"
	return res

@register.filter
def get_error(error):
	return "error"
