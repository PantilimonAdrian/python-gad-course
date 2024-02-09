"""
URL configuration for gametracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from games_journal.views import (homepage, profilepage,
                                 addgamepage, updategameinfo,
                                 removegame)
from members.views import register_user_page, login_user_page, logout_user_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", homepage, name="home"),

    # Account management paths
    path("register/", register_user_page, name="register_user"),
    path("login/", login_user_page, name="login_user"),
    path("logout/", logout_user_page, name="logout_user"),

    # CRUD operations
    path("profile/", profilepage, name="profile_page"),
    path("add-game/", addgamepage, name="add_game_page"),
    path("update-game-info/", updategameinfo, name="update_game_page"),
    path("remove-game/", removegame, name="remove_game_page"),
]
