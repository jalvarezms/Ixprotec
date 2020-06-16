from django import forms
from apps.publications.models import  Article, Comment
from django.utils.translation import ugettext as _
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title', 
            'short_description',    
            'profile_picture',
            'categories',
            'status',
            'start_date',
            'end_date',
            'body_message',
            'author'
        ]
        labels = {
            'title':_('Title'), 
            'short_description':_('Short Description'),   
            'profile_picture':_('Profile Picture'),
            'categories':_('Categories'),
            'status':_('Status'),
            'start_date':_('Start Date'),
            'end_date':_('End Date'),
            'body_message':_('Body Message'),
            'author':''
        }
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'short_description':forms.Textarea(attrs={'class':'form-control', 'rows':'2'}),
            'profile_picture': forms.FileInput(attrs={'class':'form-control-file form-control-sm'}),     
            'categories': forms.SelectMultiple(attrs={'class':'form-control ec-tags', 'multiple' : 'multiple'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'start_date': forms.TextInput(attrs={'class':'form-control datepicker', 'data-date-format':'dd-mm-yyyy'}),
            'end_date': forms.TextInput(attrs={'class':'form-control datepicker', 'data-date-format':'dd-mm-yyyy'}),
            'body_message':SummernoteWidget(),
            'author':forms.TextInput(attrs={'class':'form-control'}),

        }