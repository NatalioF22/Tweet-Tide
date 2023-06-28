from django import forms 
from. models import Meep, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#profile extras
class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture")
    profile_bio = forms.CharField(label="Profile Bio",widget= forms.Textarea(attrs={'class':'form-control','placeholder':'Profile Bio'}))
    homepage_link= forms.CharField(label="Website Link",widget= forms.TextInput(attrs={'class':'form-control','placeholder':'Website Link'}))
    facebook_link = forms.CharField(label="Facebook link",widget= forms.TextInput(attrs={'class':'form-control','placeholder':'Facebook link'}))
    instagram_link = forms.CharField(label="Instagram link",widget= forms.TextInput(attrs={'class':'form-control','placeholder':'Instagram link'}))
    linkedIn_link = forms.CharField(label="LinkediN link",widget= forms.TextInput(attrs={'class':'form-control','placeholder':'LinkedIn link'}))
    
    
    class Meta:
        model = Profile
        fields = ("profile_image", "profile_bio","homepage_link", "facebook_link","instagram_link", "linkedIn_link", )

class MeepForm(forms.ModelForm):
    body= forms.CharField(required=True,
                          widget=forms.widgets.Textarea(attrs={
        "placeholder":"Enter your Musker Meep",
        "class":"form-control",
    }),
    label="")
    class Meta:
        model = Meep
        exclude = ("user","likes", )

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="",widget= forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    first_name = forms.CharField(label="",max_length=100,widget= forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name = forms.CharField(label="",max_length=100,widget= forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Your User Name'
        self.fields['username'].label = ""
        self.fields['username'].help_text = "<span class='form-text text-muted'><small>Required. 150 character or fewer. Letters digits and symbols.</small></span>"
        
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ""
        self.fields['password1'].help_text = "<span class='form-text text-muted'><small>Your password must be at least 8 characters long. It must contains aty least 2 digits, 2 letters and 2 symbols</small></span>"
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Password Confirmation'
        self.fields['password2'].label = ""
        self.fields['password2'].help_text ="<span class='form-text text-muted'><small>Enter the same Password</small></span>"
        
    def clean_username(self):
        username = self.cleaned_data['username']
        current_user = self.instance
        if User.objects.exclude(pk=current_user.pk).filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        return username
