from django import forms

class PersonSearchForm(forms.Form):
    search_field = forms.CharField(max_length=100)
