"""d3leaderboards URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from core.views import LeaderboardList, LeaderboardDetail, RecordList, RecordDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('leaderboards/', LeaderboardList.as_view()),
    path('leaderboards/<str:slug>', LeaderboardDetail.as_view()),
    path('records/', RecordList.as_view()),
    path('records/<int:pk>', RecordDetail.as_view()),

]
