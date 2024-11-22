from .views import *
from django.urls import path

urlpatterns = [
    path('', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('home/', home, name='home'),
    path('create/', create_product, name= 'create'),
    path('updateproduct/<int:product_id>', update_product, name= 'update'),
    path('deleteproduct/<int:product_id>', delete_product, name='delete'),
    path('profile/', UserProfile, name='profile'),
    path('deletepic/', delete_profile_pic, name="delete")
]