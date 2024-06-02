from django.contrib import admin
from django.urls import path
from . import views
from .views import logout_view, cart_view, add_to_cart
urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('products/', views.product_list_view, name='products'),
    path('cart/', views.cart_view, name='cart'),
    path('admin/', admin.site.urls),
    path('logout/', logout_view, name='logout'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('place_order/', views.place_order, name='place_order'),
]