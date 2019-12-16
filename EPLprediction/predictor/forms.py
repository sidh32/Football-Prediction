from django import forms

class HomeForm(forms.Form):
	Hometeam = forms.CharField()
	Awayteam = forms.CharField()