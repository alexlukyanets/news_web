from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = 'home'),
    path('catеgory/<int:category_id>/', get_category, name = 'category'),
]