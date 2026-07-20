from django.shortcuts import render, redirect
from .models import Product, Category
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from reviews.models import Review
from dashboard.models import PurchaseItem

def home(request):
    featured_products = Product.objects.filter(featured=True, available=True)[:4] #Search the Product table and return the first 4 products in which featured=True and available=True
    context = {"featured_products": featured_products}
    return render(request, 'home/home.html', context)

def products(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    selected_category = request.GET.get("category")
    search_query = request.GET.get("search")
    if selected_category:
        products = products.filter(subcategory__category__name=selected_category)
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(brand__icontains=search_query) | Q(subcategory__name__icontains=search_query) | Q(subcategory__category__name__icontains=search_query)).distinct()
    context = {"products": products, "categories": categories, "selected_category": selected_category, "search_query": search_query}
    return render(request, 'products/products.html', context)

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = []
    for review in product.reviews.all():
        reviews.append({

            "user": review.user.username,
            "rating": review.rating,
            "comment": review.comment,
            "date": review.date_created.strftime("%d %b %Y")

        })
    related_products = []
    related = Product.objects.filter(subcategory__category=product.subcategory.category).exclude(id=product_id).order_by("-featured", "name")[:3]
    for item in related:
        related_products.append({

            "id": item.id,
            "name": item.name,
            "brand": item.brand,
            "price": str(item.price),
            "rating": item.average_rating(),
            "image": item.image.url if item.image else ""

        })
    can_review = False
    already_reviewed = False
    review_message = ""

    if request.user.is_authenticated:

        already_reviewed = Review.objects.filter(user=request.user, product=product).exists()

        purchased = PurchaseItem.objects.filter(purchase__user=request.user, product=product).exists()

        if already_reviewed:

            review_message = "You have already reviewed this product."

        elif purchased:

            can_review = True

        else:

            review_message = "Only customers who have purchased this product can leave a review."

    else:

        review_message = "Please log in to leave a review."

    data = {

        "id": product.id,
        "name": product.name,
        "brand": product.brand,
        "category": product.subcategory.category.name,
        "price": str(product.price),
        "description": product.description,
        "rating": product.average_rating(),
        "review_count": product.review_count(),
        "image": product.image.url if product.image else "",
        "stock": product.stock_quantity,
        "reviews": reviews,
        "related_products": related_products,
        "can_review": can_review,
        "already_reviewed": already_reviewed,
        "review_message": review_message,

    }
    return JsonResponse(data)

def about(request):

    return render(request, 'about/about.html')

def contact(request):

    if request.method == 'POST':

        messages.success(request, 'Thank you for contacting The Pet Corner! We have received your message and will get back to you as soon as possible.')

        return redirect('contact')

    return render(request, 'contact/contact.html')