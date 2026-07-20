from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Cart, CartItem
from products.models import Product

@login_required
def cart(request):
    
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items = cart.items.select_related("product")

    total = sum(

        item.product.price * item.quantity 

        for item in cart_items 

    )

    context = {'cart': cart, 'cart_items': cart_items, 'total': total}

    return render(request, 'cart/cart.html', context)

@require_POST
def add_to_cart(request):

    if not request.user.is_authenticated:

        return JsonResponse(

            {

                'success': False,
                'login_required': True,
                'message': 'Please login or register to add products to your cart.'

            },
            status=401

        )

    product_id = request.POST.get('product_id')

    quantity = int(request.POST.get('quantity', 1))

    try: 
        
        product = Product.objects.get(id=product_id)

    except Product.DoesNotExist:

        return JsonResponse(

            {

                'success': False, 'message': "Product not found."

            },
            status=404

        )
    
    #Check that requested quantity does not exceed available quantity
    if quantity > product.stock_quantity:

        return JsonResponse(

            {

                'success': False, 'message': f"Only {product.stock_quantity} item(s) available in stock."

            },
            status=400

        )
    
    #Create customer's cart if it does not exist
    cart, created = Cart.objects.get_or_create(user=request.user)

    #Check if product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})

    #Increase quantity
    if not created:

        new_quantity = cart_item.quantity + quantity

        if new_quantity > product.stock_quantity:

            return JsonResponse(

                {

                    'success': False, 'message': f"Only {product.stock_quantity} item(s) available in stock."

                },
                status=400

            )

        cart_item.quantity = new_quantity
        cart_item.save()

    #Total quantity of all items
    cart_count = sum(item.quantity for item in cart.items.all())

    return JsonResponse(

        {'success': True, 'message': "Item has been added to cart!", 'cart_count': cart_count}

    )

@login_required
@require_POST
def update_cart(request):
    
    product_id = request.POST.get("product_id")

    action = request.POST.get("action")

    cart = Cart.objects.get(user=request.user)

    try:

        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)

    except CartItem.DoesNotExist:

        return JsonResponse(

            {

                'success': False, 'message': "Cart item not found."

            },
            status=404

        )
    
    if action == 'increase':

        if cart_item.quantity >= cart_item.product.stock_quantity:

            return JsonResponse(

                {

                    'success': False, 'message': f"Only {cart_item.product.stock_quantity} item(s) available in stock."

                },
                status=400

            )
        
        cart_item.quantity += 1

    elif action == 'decrease':

        cart_item.quantity -= 1

    elif action == 'remove':

        removed = True

        cart_item.delete()

    else:

        return JsonResponse(

            {

                'success': False, 'message': "Invalid action."

            }

        )

    removed = False

    if action == 'remove':

        removed = True

    elif cart_item.quantity <= 0:

        removed = True

        cart_item.delete()

    else:

        cart_item.save()

    cart_items = cart.items.select_related("product")

    cart_total = sum(

        item.subtotal

        for item in cart_items

    )

    cart_count = sum(

        item.quantity

        for item in cart_items

    )

    return JsonResponse(

        {

            'success': True, 'removed': removed, 'quantity': cart_item.quantity if not removed else 0, 'subtotal': float(cart_item.subtotal) if not removed else 0, 'cart_total': float(cart_total), 'cart_count':  cart_count            

        }

    )