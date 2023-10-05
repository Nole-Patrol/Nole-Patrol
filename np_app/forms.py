from django import forms

class EmailSearchForm(forms.Form):
    email = forms.EmailField(label="Email")
