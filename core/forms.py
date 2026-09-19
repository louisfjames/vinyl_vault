from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Name')
    email = forms.EmailField(label='Email Address')
    phone_number = forms.CharField(max_length=20, label='Telephone', required=False)
    message = forms.CharField(widget=forms.Textarea, label='Reason for Contacting')
