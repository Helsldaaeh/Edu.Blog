from django import forms

class UserForm(forms.form):
    username = forms.CharField(
        max_length=150,
        
    ) 
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput,
    ) 
