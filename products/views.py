from django.shortcuts import render, redirect
from .models import Product, Order


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def cart(request):
    cart_ids = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart_ids)

    total = sum(product.price for product in products)

    return render(request, 'cart.html', {
        'products': products,
        'total': total
    })


def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id not in cart:
        cart.append(product_id)

    request.session['cart'] = cart

    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id in cart:
        cart.remove(product_id)

    request.session['cart'] = cart

    return redirect('cart')


def checkout(request):
    if request.method == 'POST':
        Order.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address')
        )

        request.session['cart'] = []

        return render(request, 'checkout.html', {
            'message': 'Order placed successfully!'
        })

    return render(request, 'checkout.html')