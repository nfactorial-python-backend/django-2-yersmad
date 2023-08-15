from django import forms

class UpdateNewsForm(forms.Form):
    title = forms.CharField(max_length=50)
    content = forms.CharField(max_length=150)
