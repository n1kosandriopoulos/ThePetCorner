from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from dashboard.models import Purchase, PurchaseItem

@login_required
def checkout(request):

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items = cart.items.select_related("product")

    total = sum(

        item.subtotal

        for item in cart_items

    )

    if request.method == "POST":

        full_name = request.POST.get('full_name', '').strip()

        email = request.POST.get("email", "").strip()
    
        phone = request.POST.get("phone", "").strip()
    
        address = request.POST.get("address", "").strip()
    
        city = request.POST.get("city", "").strip()
    
        postal_code = request.POST.get("postal_code", "").strip()

        if not all([full_name, email, phone, address, city, postal_code]):

            context = {

                'cart': cart,
                'cart_items': cart_items,
                'total': total,
                'error': "Please fill in all required fields."

            }

            return render(request, 'checkout/checkout.html', context)
        
        for item in cart_items:

            if item.quantity > item.product.stock_quantity:

                context = {

                    'cart': cart,
                    'cart_items': cart_items,
                    'total': total,
                    'error': f'Sorry, only {item.product.stock_quantity} unit(s) of {item.product.name} are currently available.'

                }

                return render(request, 'checkout/checkout.html', context)

        purchase = Purchase.objects.create(user=request.user, total_amount=total, full_name=full_name, email=email, phone=phone, address=address, city=city, postal_code=postal_code)

        for item in cart_items:

            PurchaseItem.objects.create(purchase=purchase, product=item.product, quantity=item.quantity, price=item.product.price)

            item.product.stock_quantity -= item.quantity

            if item.product.stock_quantity == 0:

                item.product.available = False

            item.product.save()

        cart.items.all().delete()

        return redirect('checkout_success')

    context = {

        'cart': cart,
        'cart_items': cart_items,
        'total': total

    }

    return render(request, 'checkout/checkout.html', context)

@login_required
def checkout_success(request):

    return render(request, 'checkout/success.html')