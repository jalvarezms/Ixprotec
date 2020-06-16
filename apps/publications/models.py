from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext as _
from datetime import datetime
# Create your models here.


class NewsClass(models.Model):
    name =  models.CharField(unique=True,max_length=30, null=False, blank=False)
    description =  models.CharField(max_length=400)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.name 

class Article(models.Model):

    UNPUBLISHED = 0
    PUBLISHED= 1   
    STATUS_CHOICES = [(UNPUBLISHED, 'Unpublished'), (PUBLISHED, 'Published')]

    title = models.CharField(max_length=120, null=False, blank=False, default=_('Title Default'))
    short_description =  models.CharField(max_length=255, null=False, blank=False, default=_('Short description default'))
    profile_picture = models.ImageField(upload_to='uploads/publications/news/', null=True, blank=True, verbose_name='profile_picture')
    categories = models.ManyToManyField(NewsClass, blank=True, related_name='categories')
    status =   models.IntegerField(choices=STATUS_CHOICES, default=PUBLISHED)
    start_date =  models.DateField(default=datetime.now)
    end_date =  models.DateField(default=datetime.strptime("9999-12-31","%Y-%m-%d"))
    body_message = models.TextField(null=True) 
    author  = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    visits = models.IntegerField( default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
       return '%s-%s-%s %s' % (self.title,self.status, self.start_date,self.author )

    def count_comments(self):
        return self.comment_set.filter(status=True).count()   

    def count_likes(self):
        return self.likepost_set.count()     


class Comment(models.Model):
    post  = models.ForeignKey(Article, null=True, blank=True, on_delete=models.SET_NULL)
    comment  = models.TextField(null=True) 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
       return '%s(%s):%s ' % (self.post,self.author, self.create_date)



class LikePost(models.Model):
    post  = models.ForeignKey(Article, null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
       return '%s(%s):%s ' % (self.post,self.author, self.create_date)       

class LikeComments(models.Model):
    post  = models.ForeignKey(Article, null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
       return '%s(%s):%s ' % (self.post,self.author, self.create_date)      

class DisLikeComments(models.Model):
    post  = models.ForeignKey(Article, null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
       return '%s(%s):%s ' % (self.post,self.author, self.create_date)       


