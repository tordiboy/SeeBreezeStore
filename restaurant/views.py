from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Meal, Cart, CartItem
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order, OrderItem



def home(request):
    meals = Meal.objects.filter(available=True)
    return render(request, 'restaurant/home.html', {'meals': meals})



def meal_detail(request, slug):
    meal = get_object_or_404(Meal, slug=slug)
    return render(request, 'restaurant/meal_detail.html', {'meal': meal})



@login_required
def add_to_cart(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, meal=meal)

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')



@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    total = sum(item.get_total_price() for item in cart.items.all())

    return render(request, 'restaurant/cart.html', {
        'cart': cart,
        'total': total
    })



def menu_view(request):
    meals = Meal.objects.filter(available=True)
    return render(request, 'restaurant/menu.html', {'meals': meals})



# This part is for login and sign up view
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = SignUpForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')

    return render(request, 'restaurant/signup.html', {'form': form})



def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('home')

    return render(request, 'restaurant/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('home')



# Checkout page for this project
@login_required
def checkout_view(request):
    cart = Cart.objects.get(user=request.user)

    if request.method == 'POST':

        full_name = request.POST['full_name']
        address = request.POST['address']
        phone = request.POST['phone']

        total = sum(item.get_total_price() for item in cart.items.all())

        # Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            phone=phone,
            total_price=total
        )

        # Move cart items → order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                meal=item.meal,
                price=item.meal.price,
                quantity=item.quantity
            )

        # Clear cart
        cart.items.all().delete()

        return redirect('track_order', order_id=order.id)

    return render(request, 'restaurant/checkout.html', {'cart': cart})

def success_view(request):
    return render(request, 'restaurant/success.html')



# This part for admin login only
@staff_member_required
def admin_orders_view(request):
    orders = Order.objects.all().order_by('-created')
    return render(request, 'restaurant/admin_orders.html', {'orders': orders})



@staff_member_required
def admin_order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    items = order.items.all()

    return render(request, 'restaurant/admin_order_detail.html', {
        'order': order,
        'items': items
    })



from django.shortcuts import get_object_or_404

@staff_member_required
def update_order_status(request, order_id, status):
    order = get_object_or_404(Order, id=order_id)

    order.status = status
    order.save()

    return redirect('admin_orders')



from django.shortcuts import render, get_object_or_404
from .models import Order

@login_required
def track_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'restaurant/track_order.html', {'order': order})



@login_required
def user_orders_view(request):
    orders = Order.objects.filter(
        user=request.user,
        status='delivered'
    ).order_by('-created')

    return render(request, 'restaurant/user_orders.html', {
        'orders': orders
    })



@staff_member_required
def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()
    return redirect('admin_orders')



from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def ajax_update_status(request, order_id):
    order = Order.objects.get(id=order_id)
    status = request.GET.get('status')

    if status:
        order.status = status
        order.save()

    return JsonResponse({'success': True, 'status': order.status})



from django.db.models import Sum, Count

@staff_member_required
def dashboard_view(request):
    orders = Order.objects.all()

    total_orders = orders.count()
    total_revenue = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

    pending = orders.filter(status='pending').count()
    delivered = orders.filter(status='delivered').count()

    return render(request, 'restaurant/dashboard.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending': pending,
        'delivered': delivered
    })

