from django import forms

class ContactForm(forms.Form):
    
    issue = forms.CharField(max_length=350)
    name = forms.CharField(required=True, max_length=200)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea,max_length=None)
