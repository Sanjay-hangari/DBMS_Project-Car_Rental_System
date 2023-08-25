from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.home),
    path('dsignup',views.dsignup),
    path('dlogin',views.dlogin),
    path('dhome',views.dhome),
    path('clogin',views.clogin),
    path('csignup',views.csignup),
    path('search',views.search),
    path('booking',views.booking),
    path('conform',views.conform),
    path('book',views.book),
    path('about',views.about),
    path('contact',views.contact),
    path('manage',views.manage),
    path('success',views.succes),
    path('history',views.history),
    path('managee',views.managee),
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)