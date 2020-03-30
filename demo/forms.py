from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

pay_choice = (
('dc','Debit Card'),
('cc','Credit Card'),
('pp','Paypal'),
('sp','Stripe'),
)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email','password1','password2']

# change value with placeholder
class CheckoutForm(forms.Form):
    Name = forms.CharField(widget=forms.TextInput(attrs={'value':'Faizan'}))
    House_no = forms.CharField(widget=forms.TextInput(attrs={'value':'1221'}))
    Area = forms.CharField(widget=forms.TextInput(attrs={'value':'Sector 31'}))
    City = forms.CharField(widget=forms.TextInput(attrs={'value':'Gurgaon'}))
    State = forms.CharField(widget=forms.TextInput(attrs={'value':'Haryana'}))
    Zip = forms.IntegerField(widget=forms.TextInput(attrs={'value':'122001'}))
    Payment_option = forms.ChoiceField(widget=forms.RadioSelect(attrs={'checked':'checked'}),choices=pay_choice)
    Same_Billing_Address = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
