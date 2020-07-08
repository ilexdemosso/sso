from django import forms

class InputForm(forms.Form): 
    login = forms.CharField(max_length = 200) 
    password = forms.CharField(widget = forms.PasswordInput()) 