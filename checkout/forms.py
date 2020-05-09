from django import forms

class DonationForm(forms.Form):
	"""docstring for ContactForm"""
	name=forms.CharField(max_length=200, initial='Enter your full name')
	email=forms.EmailField(initial='type a valid email address')
	amount=forms.ChoiceField( choices=[(5, 'i Like you and your work(5$)'),(10, 'i love you and your work(10$)'),(50, 'Bro you are the best (50$)')])
