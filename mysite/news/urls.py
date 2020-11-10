from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page
urlpatterns = [
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('login/', user_login, name='login'),
    path('contact/', contact, name = 'contact'),
    #path('', index, name = 'home'),
    path('', HomeNews.as_view(), name = 'home'),
    #path('catеgory/<int:category_id>/', get_category, name = 'category'),
    path('catеgory/<int:category_id>/', NewsByCategory.as_view(), name = 'category'),
    #path('', cache_page(60)(HomeNews.as_view()) , name = 'home'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    #path('news/add-news/', add_news, name='add_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
]