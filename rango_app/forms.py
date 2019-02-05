from django import forms
from rango_app.models import Page, Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Category.name==")
    #slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    #views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Category
        fields = ('name',)


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