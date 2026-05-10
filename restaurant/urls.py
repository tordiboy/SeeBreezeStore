from django.urls import path
from . import views
from .views import signup_view, login_view, logout_view


urlpatterns = [
    path('', views.home, name='home'),
    path('meal/<slug:slug>/', views.meal_detail, name='meal_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:meal_id>/', views.add_to_cart, name='add_to_cart'),
    path('menu/', views.menu_view, name='menu'),

    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('checkout/', views.checkout_view, name='checkout'),
    path('success/', views.success_view, name='success'),

    path('dashboard/orders/', views.admin_orders_view, name='admin_orders'),
    path('dashboard/orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('dashboard/orders/<int:order_id>/status/<str:status>/', views.update_order_status, name='update_order_status'),

    path('track-order/<int:order_id>/', views.track_order_view, name='track_order'),
    path('api/update-status/<int:order_id>/', views.ajax_update_status),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('my-orders/', views.user_orders_view, name='user_orders'),
    path('dashboard/orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),
]