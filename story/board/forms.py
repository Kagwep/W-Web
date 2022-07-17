from pyexpat import model
from attr import fields
from django.forms import ModelForm
from .models import UserReg,Mystory,Genre,Episode,Series
from django.contrib.auth.forms import UserCreationForm

class SingUPForm(UserCreationForm):
    class Meta:
        model = UserReg
        fields = ['username','first_name','last_name','email','phone_number','password1','password2']

class MystoryForm(ModelForm):
    class Meta:
        model = Mystory
        fields = '__all__'
class genreForm(ModelForm):
    class Meta:
        model = Genre
        fields= '__all__'
class episodeForm(ModelForm):
    class Meta:
        model = Episode
        fields = '__all__'
class seriesForm(ModelForm):
    class meta:
        model = Series
        fields = '__all__'
