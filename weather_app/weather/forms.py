from django import forms 
class CityForm(forms.Form):
    city = forms.CharField(label = "Enter City Name", max_length = 100)