from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin
from apps.publications.models import Article,NewsClass, Comment
# Register your models here.

class ArticletAdmin(SummernoteModelAdmin):
    summernote_fields = ('body_message')

admin.site.register(Article,ArticletAdmin)
admin.site.register(NewsClass)
