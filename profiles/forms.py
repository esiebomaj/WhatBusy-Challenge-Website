from django import forms

class ContactForm(forms.Form):
	"""docstring for ContactForm"""
	name=forms.CharField(max_length=200, initial='Enter your full name')
	email=forms.EmailField(help_text='type a valid email address')
	comment=forms.CharField(max_length=200, initial='comment goes here', widget=forms.Textarea)
