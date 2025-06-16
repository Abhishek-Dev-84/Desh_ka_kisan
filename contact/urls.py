from django.contrib import admin
from django.urls import path,include
from contact import views
from django.conf import settings
from django.conf.urls.static import static
# from .views import run_migrations

urlpatterns = [
    # path('run-migrations',views.run_migrations,name='run-migrations'),
    path('',views.index,name='index'),
    path('contact',views.contact,name='contact'),
    path('help',views.help,name='help'),
    path('features',views.features,name='features'),
    path('signup',views.signup,name='signup'),
    path('buyer-login/',views.buyer_login,name='buyer-login'),
    path('buyer-login/buyer-dashboard/',views.buyer_dashboard,name = 'buyer-dashboard1'),
    path('seller-dashboard/seller-login/',views.seller_login,name = 'seller-login'),
    path('seller-login/',views.seller_login,name='seller-login'),
    path('buyer-dashboard/',views.buyer_dashboard,name='buyer-dashboard'),
    path('seller-dashboard/',views.seller_dashboard,name='seller-dashboard'),
    path('Orders/',views.Orders,name = 'Orders'),
    path('Logout/signup',views.signup,name= 'signup'),
    path('logout_buyer/signup',views.signup,name= 'signup'),
    path('logout_buyer/',views.logout_buyer,name= 'logout_buyer'),
    path('logout_buyer/index.html',views.index,name='index'),
    path('seller-login.html',views.index,name='index'),
    path('manage-listings',views.manage_listings,name='manage-listings'),
    path('order-list',views.order_list,name='order-list'),
    path('profile-Settings',views.profile_settings,name='profile-Settings'),
    path('seller/update-profile',views.update_profile,name='update-profile'),
    path('Logout',views.Logout,name='Logout'),
    path('buy/<int:product_id>/',views.buy_now,name='buy_now'),
    path('orders/',views.orders_list,name='orders_list'),
    path('seller/add-product/',views.add_product,name='add-product'),
    path('seller-dashboard/add-product/',views.add_product,name='add-product'),
    path('track_orders/<int:order_id>/',views.orders_list,name='track_order'),
    path('delete-product/<int:product_id>/',views.delete_product,name='delete_product'),
    path('buy_now/<int:product_id>/',views.buy_now,name='buy_now'),
    path('order_confirmed',views.order_confirmed, name='order_confirmed'),
    path('buyer-dashboard.html',views.buyer_dashboard,name='buyer-dashboard'),
    path('order_confirmed/<int:order_id>/', views.order_confirmed, name='order_confirmed'),
    path('add-product/',views.add_product,name='add-product'),
] + static(settings.MEDIA_URL,
           document_root = settings.MEDIA_ROOT)
