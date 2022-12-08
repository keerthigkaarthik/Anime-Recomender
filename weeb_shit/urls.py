from django.urls import path
from weeb_shit import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout,name='logout'),
    path('list_of_anime', views.lists, name='lists'),
    path('animes/<str:id>/', views.animes, name = 'animes'),
    path('profile', views.profile, name='profile' ),
    path('search/', views.search, name='search'),
    path('update',views.update,name='update'),
    path('recommend', views.index, name="recommend")
]