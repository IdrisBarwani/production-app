"""production URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path
from django.conf import settings
from manufac.views import index, start, add_wol, get_wol, LogUpdateView, recieve_data
# from django.conf.urls.static import static

admin.site.site_header = 'Production App admin'

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('manufac/', include('manufac.urls')),
    path('admin/', admin.site.urls),
    path('<int:pk>/start/', start, name='start'),
    path('<int:pk>/add_wol/', add_wol, name='add_wol'),
    path('<int:pk>/get_wol/', get_wol, name='get_wol'),
    path('<int:pk>/logUpdate/', LogUpdateView.as_view(), name='WorkOrderLog'),
    path('recieve_data/', recieve_data, name='recieve_data'),
    path('', index, name='index') #redirect to dashboard
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
