from django.shortcuts import render, redirect
from django.views.generic import ListView,TemplateView,CreateView,UpdateView,DeleteView,View, DetailView
from apps.publications.forms import ArticleCreateForm
from apps.publications.models import NewsClass,Article,Comment, LikePost,LikeComments,DisLikeComments
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from ippe.util.select_data_util import *
# Create your views here.
from datetime import date




class ListPublicationsView(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    template_name =  'articles_blogs.html'
    model = Article
    
    def get_context_data(self , **kwargs):
        context = super(ListPublicationsView,self).get_context_data(**kwargs)
        # print(self.request.user.employee)
        today = date.today()
        data = Article.objects.filter(status=Article.PUBLISHED,start_date__lte = today, end_date__gte = today ).order_by('-create_date')
        context['articles'] =  data       
        return context

class ListPublicationsAdminView(LoginRequiredMixin,ListView):
    login_url ='authenticate:login'
    template_name =  'article_list.html'
    model = Article
    
    def get_context_data(self , **kwargs):
        context = super(ListPublicationsAdminView,self).get_context_data(**kwargs)
        # print(self.request.user.employee)
        data = Article.objects.order_by('-create_date')
        context['articles'] =  data
        elements = []
        for d in data:
            elements.append([
                {
                    'type': 'text',
                    'content': d.id
                },
                 {
                    'type': 'image',
                    'content': d.profile_picture.url
                },
                {
                    'type': 'name',
                    'content': d.title 
                },
                 {
                    'type': 'text',
                    'content': d.short_description   
                },
                {
                    'type': 'categories',
                    'content': d.categories.all  
                },
                {
                    'type': 'date_short',
                    'content': d.start_date  
                },
                {
                    'type': 'date_short',
                    'content': d.end_date 
                },

                {
                    'type': 'action',
                    'actions': [
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-edit"></i> <span >'+_('Edit')+'</span>',
                            'href': reverse_lazy("publications:update_news", kwargs = {'pk': d.id})
                        },
                        {
                            'content': '<i class="fas fa-lg fa-fw m-r-10 fa-trash"></i> <span >'+_('Delete')+'</span>',
                            'href': '#',
                            'pk' : d.id,
                        }
                    ]
                }
            ])
        dataTable = {
            'card_tittle' : _('Publications'),
            'headers': ['#',_("Profile"),_('Title'),_('Description'),_('Categories'),_('Start Date'),_('End Date'),_('Options')],
            'data': elements,
            'create_button_url' : reverse_lazy("publications:create_news"),
            'delete_button_url' : reverse_lazy("publications:delete_news")
        }
        context['dataTable'] =  dataTable
        return context
       
        return context

class CreatePublicationsNewsView(LoginRequiredMixin,CreateView):
    login_url ='authenticate:login'
    model = Article
    form_class = ArticleCreateForm
    template_name = 'article_create.html'
    def get_context_data(self , **kwargs):
        context = super(CreatePublicationsNewsView, self).get_context_data(**kwargs)
        context['news_class'] = NewsClass.objects.all()
        context['employee'] = self.request.user.employee   
        categories_options =  get_newsClass_multi_select_options('')    
        context['categories_options'] = categories_options
        return context
    
    def get_success_url(self, **kwargs):
            return (reverse_lazy('publications:list_news'))

class UpdatePublicationsNewsView(LoginRequiredMixin,UpdateView):
    login_url ='authenticate:login'
    model = Article
    form_class = ArticleCreateForm
    template_name = 'article_create.html'
    def get_context_data(self , **kwargs):
        context = super(UpdatePublicationsNewsView, self).get_context_data(**kwargs)
        post = self.object  
        seleted_id = post.categories.all().values('id')
        categories_options =  get_newsClass_multi_select_options(seleted_id)    
        context['categories_options'] = categories_options
        return context
    
    def get_success_url(self, **kwargs):
            return (reverse_lazy('publications:list_news'))

class ShowPublicationsNewsView(LoginRequiredMixin,DetailView):
    login_url ='authenticate:login'
    model = Article
    template_name = 'article_show.html'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.visits  = 1 + self.object.visits
        self.object.save()
        context = self.get_context_data(object=self.object)
        
        context['comments'] = self.object.comment_set.filter(status=True).order_by('-create_date') 
        
        return self.render_to_response(context)

class DeletePublicationsNewsView(LoginRequiredMixin,View):
    login_url ='authenticate:login'
    def post(self, request, *args, **kwargs):
        pk = request.POST['delete_id']
        data = Article.objects.get(id = pk)
        data.delete()
        return redirect(reverse_lazy('publications:list_news'))

class CreateCommentNewsView(LoginRequiredMixin,View):
    login_url ='authenticate:login'
    def post(self, request, *args, **kwargs):
        comment = request.POST['comment']
        post_id =   request.POST['post']
        post = Article.objects.get(id=post_id)
        author = self.request.user
        data = Comment.objects.create(
                post= post,
                comment = comment,
                author = author
        )
        print(data)

        return render(request, 'comments_base.html', {'comments': post.comment_set.filter(status=True).order_by('-create_date') })  



class DeleteCommentNewsView(LoginRequiredMixin,View):
    login_url ='authenticate:login'
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', 0)
        comment = Comment.objects.get(id = pk)
        post = comment.post
        comment.status = False
        comment.save()
        return render(request, 'comments_base.html', {'comments': post.comment_set.filter(status=True).order_by('-create_date') })  


class CreateLikeNewsView(LoginRequiredMixin,View):
    login_url ='authenticate:login'
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', 0)
        post = Article.objects.get(id = pk)
        author = self.request.user
        data = post.likepost_set.filter(author = author).exists()
        if not data:
            data = LikePost.objects.create(
                post=post,
                author = author
            )        
        return render(request, 'footer_btn_like.html', {'article':post })

class CreateLikeCommentNewsView(LoginRequiredMixin,View):        
    login_url ='authenticate:login'
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', 0)
        comment = Comment.objects.get(id = pk)
        author = self.request.user
        data = comment.likecomments_set.filter(author = author).exists()
        if not data:
            data = LikeComments.objects.create(
                post=post,
                author = author
            )
        return render(request, 'footer_btn_like.html', {'comments': post.comment_set.filter(status=True).order_by('-create_date') })