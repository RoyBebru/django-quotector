from django.urls import path
from . import views


app_name = 'quoteapp'


urlpatterns = [
    path('', views.main, name='main'),
    path('page/<int:page_num>/', views.main, name='main_page'),
    path('page/<int:page_num>/<str:with_tag>/', views.main, name='main_page_tag'),
    path('author/', views.author, name='author'),
    path('about/<str:fullname>/', views.about, name='about'),
    path('quote/', views.quote, name='quote'),
    path('quote/<str:author>/', views.quote, name='quote_author'),
    path('tag/', views.tag, name='tag'),
    path('scrapy_content/', views.scrapy_content, name='scrapy_content'),
]
