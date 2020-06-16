from django.conf.urls import url
from django.urls import  include, path
from django.views.generic import TemplateView
from .views import indexViews, NotificationsView,Dashboard
from django.conf import settings
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    # path('', indexViews.as_view(), name='index'),
    path('', Dashboard.as_view(), name='index'),
    path('notifications/view/<int:pk>', NotificationsView.as_view(), name='notification_view'),
    # path('dashboard', Dashboard.as_view(), name='dashboard' ),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
