from django.urls import path
from store import views
from django.contrib.auth import views as auth_views
from .forms import CustomerLoginForm
urlpatterns =[
    path('', views.ProductView.as_view(), name='index'),
    path('product-details/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    # Authentication

    path('registration/', views.CustomerRegistrationView.as_view(), name='customer-registration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='customer-login.html', authentication_form=CustomerLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),name='customer-logout'),

    # customer profile 

    path('profile/', views.ProfileView.as_view(), name = 'profile'),

    # address

    path('address/', views.Address, name='address'),

    # cart
    path('add-to-cart/', views.cart,name='add-to-cart'),
    path('cart/', views.display_cart, name='show-cart'),


    path('pluscart/', views.plus_cart, name='plus-cart'),
    path('minuscart/', views.minus_cart, name='minus-cart'),
    path('removecart/', views.remove_cart, name='remove-cart'),

    # checkout 
    path('checkout/', views.checkout, name='checkout'),

    #payment done

    path('paymentdone/', views.payment_done, name='payment-done'),

    # orders status 

    path('orders/', views.orders, name='orders'),

] 
