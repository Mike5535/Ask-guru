"""askguru URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('questionsSort/<str:sort>', views.index),
    path('ask/', views.ask),
    path('login/', views.login),
    path('settings/', views.settings),
    path('registration/', views.registration),
    path('answer/<int:id_question>', views.answer),
    path('questionsByTag/<str:tag>', views.index),
    path('logout/', views.logout),
    path('vote/', views.vote, name='vote-view')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
