"""ippe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
import notifications.urls
from django.contrib.staticfiles import views
from django.urls import re_path
from django.views.i18n import JavaScriptCatalog
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.base.urls', namespace='base')),
    path('login/', include('apps.authenticate.urls')),
    path('elements/', include('apps.elements.urls', namespace='elements')),
    path('sizes/', include('apps.sizes.urls', namespace='sizes')),
    path('requests/', include('apps.requests.urls', namespace='requests')),
    path('equipments/', include('apps.equipments.urls', namespace='equipments')),
    path('warehouses/', include('apps.warehouses.urls', namespace='warehouses')),
    #path('providers/', include('apps.inventories.urls', namespace='inventories')),
    path('employees/', include('apps.employees.urls', namespace='employees')),
    path('inventories/', include('apps.inventories.urls', namespace='inventories')),
    path('assignments/', include('apps.assignments.urls', namespace='assignments')),
    path('reports/', include('apps.reports.urls', namespace='reports')),
    path('publications/', include('apps.publications.urls', namespace='publications')),
    path('summernote/', include('django_summernote.urls')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),

    path('api/v1/', include('apps.api.urls')),

    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('i18n/', include('django.conf.urls.i18n')),
]


if settings.DEBUG:
    
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', views.serve),
    ]
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)