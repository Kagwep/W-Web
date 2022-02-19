from django.forms import ModelForm
from .models import UserReg,Mystory
from django.contrib.auth.forms import UserCreationForm

class SingUPForm(UserCreationForm):
    class Meta:
        model = UserReg
        fields = ['username','first_name','last_name','email','phone_number','password1','password2']

class MystoryForm(ModelForm):
    class Meta:
        model = Mystory
        fields = '__all__'