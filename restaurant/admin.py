from django.contrib import admin
from .models import Category, Meal, Order, OrderItem, User

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Meal)
admin.site.register(Order)
admin.site.register(OrderItem)