from django.urls import path

from . import views

app_name = 'CloaksMart'

urlpatterns = [
    #path("", views.index, name="index"),
    path("marketplace/<str:sort_by>", views.listings, name="listings"),
    path("marketplace/", views.listings, name="listings"),
    #path("create_trade_request/", views.create_trade_request, name="create_trade_request"),
    #path("create_trade_request/", views.login_api, name="login_api"),
    #path('home/', views.home, name='home'),
    #path('request_message', views.request_message, name='request_message'),
    #path('verify_message', views.verify_message, name='verify_message'),
    path('clan_lookup/', views.my_profile, name='my_profile'),
    #path('forum_home', views.forum_home, name='forum_home'),
    #path('forum_detail', views.forum_detail, name='forum_detail'),
    #path('forum_posts', views.forum_posts, name='forum_posts'),
    path('codex/', views.codex, name='codex'),
    #path('collage_maker/', views.collage_maker, name='collage_maker'),
   
]
