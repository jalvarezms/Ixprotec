from django.conf.urls import url
from django.urls import  include, path
from django.conf import settings
from django.conf.urls.static import static

from apps.publications.views import ListPublicationsAdminView,ListPublicationsView, CreatePublicationsNewsView, UpdatePublicationsNewsView, ShowPublicationsNewsView, DeletePublicationsNewsView, CreateCommentNewsView,  DeleteCommentNewsView,CreateLikeNewsView,CreateLikeCommentNewsView

app_name = 'publications'
urlpatterns = [
    path('list/admin/news',ListPublicationsAdminView.as_view(),name="list_news_admin"),
    path('list/news',ListPublicationsView.as_view(),name="list_news"),
    path('create/news',CreatePublicationsNewsView.as_view(),name="create_news"),
    path('create/like/news/<int:pk>',CreateLikeNewsView.as_view(),name="create_like_news"),
    path('update/news/<int:pk>',UpdatePublicationsNewsView.as_view(),name="update_news"),
    path('show/news/<int:pk>',ShowPublicationsNewsView.as_view(),name="show_news"),
    path('delete/news',DeletePublicationsNewsView.as_view(),name="delete_news"),

    path('create/comments',CreateCommentNewsView.as_view(),name="create_comments"),
    path('create/like/comments',CreateLikeCommentNewsView.as_view(),name="create_like_comments"),

    path('delete/comments/<int:pk>',DeleteCommentNewsView.as_view(),name="delete_comments"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)