from django import forms
from django.contrib.auth.models import User
from rango_app.models import Page, Category, UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Category.name==")
    # slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    #views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Category
        fields = ('name',)


#TODO: fix url cleaned data here and in profile
class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Page.name==")
    url = forms.URLField(max_length=200, help_text="Page.url==")
    #views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    #date

    class Meta:
        model = Page
        fields = ('title','url')
        #or 
        #exclude = ('category','views'...)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

        
class UserProfileForm(forms.ModelForm):
    YEAR_CHOICES = range(1800,2300)
    birth_date = forms.DateField(widget=forms.SelectDateWidget(
                                years=YEAR_CHOICES))
    
    class Meta:
        model = UserProfile
        fields = ('website', 'avatar', 'birth_date', 'gender')