from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from .forms import HomeForm
from django.contrib import messages
# Create your views here.



def home(request):
	import pickle
	form_value= HomeForm
	form = form_value(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			Hometeam = form.cleaned_data['Hometeam']
			Awayteam = form.cleaned_data['Awayteam']
			print(Hometeam,Awayteam)
			b= doPrediction(Hometeam,Awayteam)
			print(b)
			if b[0]=="W":
				winner = 'Home Team'
			elif b[0]=="D":
				winner = 'Draw'
			else:
				winner = 'Away Team'
			messages.info(request, str(winner))
	return render(request,'index.html', {'form':form})

def land(request):
	return render(request, 'index.html')


def loadFile(Hometeam,Awayteam):
	import pickle
	import pandas as pd
	data= pd.read_csv('C:/Users/sidht/FYP/EPLprediction/final_dataset1.csv')
	ht= Hometeam
	at= Awayteam
	hm= data["HomeTeam"]
	hp= 0
	for i in hm:
		if i == ht:
			hp = hp + 1
	am= data["AwayTeam"]
	ap= 0
	for i in am:
		if i == at:
			ap = ap + 1
	
	a= (data[data["HomeTeam"] == ht].sum().HTP)/hp
	b= (data[data["AwayTeam"] == at].sum().ATP)/ap
	c= (data[data["HomeTeam"] == ht].sum().HomeTeamLP)/hp
	d= (data[data["AwayTeam"] == at].sum().AwayTeamLP)/ap
	e= (data[data["HomeTeam"] == ht].sum().HTFormPts)/hp
	f= (data[data["AwayTeam"] == at].sum().ATFormPts)/ap
	g= (data[data["HomeTeam"] == ht].sum().HTGD)/hp
	h= (data[data["AwayTeam"] == at].sum().ATGD)/ap
	feature =[a],[b],[c],[d],[e],[f],[g],[h]	
	return feature


def loadModel(p):
	import pandas as pd
	import pickle
	try:
		predictionModel = pickle.load(open('C:/Users/sidht/FYP/EPLprediction/xgbPredictionModel.sav','rb'))
	except:
		print("File is not loaded")
	print(p[0])
	d = {'HTP': p[0],'ATP': p[1],'HomeTeamLP': p[2],'AwayTeamLP': p[3],'HTFormPts': p[4],'ATFormPts': p[5], 'HTGD': p[6],'ATGD': p[7]}
	df = pd.DataFrame(data=d)
	print(df)
	result= predictionModel.predict(df)
	print(result)
	return result


def doPrediction(Hometeam,Awayteam):
	import pickle
	a = loadFile(Hometeam,Awayteam)
	result = loadModel(a)
	print (result)
	return result

	
