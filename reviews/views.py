from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Review
from products.models import Product
from dashboard.models import PurchaseItem


@login_required
@require_POST
def submit_review(request):

    product_id = request.POST.get('product_id')
    rating = request.POST.get('rating')
    comment = request.POST.get('comment', '').strip()

    if not rating:

        return JsonResponse(
            {
                'success': False,
                'message': 'Please select a rating.'
            },
            status=400
        )

    product = Product.objects.get(id=product_id)

    purchased = PurchaseItem.objects.filter(purchase__user=request.user, product=product).exists()

    if not purchased:

        return JsonResponse(
            {
                'success': False,
                'message': 'Only customers who purchased this product can leave a review.'
            },
            status=403
        )

    if Review.objects.filter(user=request.user, product=product).exists():

        return JsonResponse(
            {
                'success': False,
                'message': 'You have already reviewed this product.'
            },
            status=400
        )

    Review.objects.create(user=request.user, product=product, rating=int(rating), comment=comment)

    return JsonResponse(
        {
            'success': True,
            'message': 'Thank you! Your review has been submitted.'
        }
    )