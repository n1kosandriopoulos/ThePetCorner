from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Purchase
from products.models import Product, Category, SubCategory
from reviews.models import Review
from accounts.models import UserProfile
from products.forms import ProductForm, CategoryForm, SubCategoryForm
from reviews.models import Review
from reviews.forms import ReviewForm
from accounts.models import UserProfile
from accounts.forms import CustomerEditForm, EmployeeCreationForm, EmployeeEditForm
from django.contrib import messages

@login_required
def my_orders(request):

    purchases = Purchase.objects.filter(user=request.user).prefetch_related('items__product')

    context = {

        'purchases': purchases,

    }

    return render(request, 'dashboard/my_orders.html', context)

@login_required
def my_reviews(request):

    reviews = (Review.objects.filter(user=request.user).select_related('product').order_by('-date_created'))

    context = {

        'reviews': reviews,

    }

    return render(request, 'dashboard/my_reviews.html', context)

@login_required
def my_profile(request):

    profile = request.user.profile

    if request.method == 'POST':

        form = CustomerEditForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():

            form.save()

            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']

            request.user.save()

            messages.success(request, 'Profile updated successfully!')

            return redirect('my_profile')

    else:

        form = CustomerEditForm(instance=profile)

        form.fields['first_name'].initial = request.user.first_name
        form.fields['last_name'].initial = request.user.last_name
        form.fields['email'].initial = request.user.email

    return render(request, 'dashboard/my_profile.html', {'form': form})

@login_required
def order_details(request, purchase_id):

    purchase = get_object_or_404(Purchase.objects.prefetch_related('items__product'), id=purchase_id, user=request.user)

    context = {

        'purchase': purchase,

    }

    return render(request, 'dashboard/order_details.html', context)

@login_required
def dashboard_home(request):

    role = request.user.profile.role

    context = {

        'role': role,

    }

    if role == 'Administrator':

        context.update({

            'products_count': Product.objects.count(),
            'categories_count': Category.objects.count(),
            'customers_count': UserProfile.objects.filter(role='Customer').count(),
            'employees_count': UserProfile.objects.filter(role='Employee').count(),
            'orders_count': Purchase.objects.count(),
            'reviews_count': Review.objects.count(),

        })

    return render(request, 'dashboard/dashboard_home.html', context)

@login_required
def manage_orders(request):

    # Only Employees and Administrators can access this page
    if request.user.profile.role not in ['Employee', 'Administrator']:

        return redirect('dashboard')

    purchases = Purchase.objects.select_related('user').order_by('-purchase_date')

    context = {

        'purchases': purchases,

    }

    return render(request, 'dashboard/manage_orders.html', context)

@login_required
def manage_order_details(request, purchase_id):

    if request.user.profile.role not in ['Employee', 'Administrator']:

        return redirect('dashboard')

    purchase = get_object_or_404(Purchase.objects.prefetch_related('items__product'), id=purchase_id)

    if request.method == 'POST':

        purchase.status = request.POST.get("status")

        purchase.save()

        return redirect('manage_order_details', purchase_id=purchase_id)

    context = {

        'purchase': purchase,

    }

    return render(request, 'dashboard/manage_order_details.html', context)

@login_required
def manage_products(request):

    if request.user.profile.role not in ['Employee', 'Administrator']:

        return redirect('dashboard')

    products = Product.objects.select_related('subcategory').order_by('name')

    context = {

        'products': products,

    }

    return render(request, 'dashboard/manage_products.html', context)

@login_required
def add_product(request):

    if request.user.profile.role not in ['Employee', 'Administrator']:
        
        return redirect('dashboard')

    if request.method == 'POST':

        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():

            product = form.save(commit=False)

            if product.stock_quantity > 0:

                product.available = True

            else:

                product.available = False

            product.save()

            messages.success(request, 'Product added successfully!')

            return redirect('manage_products')

    else:

        form = ProductForm()

    return render(request, 'dashboard/add_product.html', {'form': form})

@login_required
def edit_product(request, product_id):

    if request.user.profile.role not in ['Employee', 'Administrator']:
        return redirect('dashboard')

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':

        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():

            product = form.save(commit=False)

            if product.stock_quantity > 0:

                product.available = True

            else: 

                product.available = False

            product.save()

            messages.success(request, 'Product updated successfully!')

            return redirect('manage_products')

    else:

        form = ProductForm(instance=product)

    return render(request, 'dashboard/edit_product.html',
        
        {
            'form': form,
            'product': product,
        },
    )

@login_required
def delete_product(request, product_id):

    if request.user.profile.role not in ['Employee', 'Administrator']:
        return redirect('dashboard')

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':

        product.delete()

        messages.success(request, 'Product deleted successfully!')

        return redirect('manage_products')

    return render(request, 'dashboard/delete_product.html', {'product': product})

@login_required
def manage_categories(request):

    if request.user.profile.role not in ['Employee', 'Administrator']:
        
        return redirect('dashboard')

    categories = Category.objects.all().order_by('name')

    return render(request, 'dashboard/manage_categories.html', {'categories': categories})

@login_required
def add_category(request):

    if request.user.profile.role not in ['Employee', 'Administrator']:
        
        return redirect('dashboard')

    if request.method == 'POST':

        form = CategoryForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'Category added successfully!')

            return redirect('manage_categories')

    else:

        form = CategoryForm()

    return render(request, 'dashboard/add_category.html', {'form': form})

@login_required
def edit_category(request, category_id):

    if request.user.profile.role not in ['Employee', 'Administrator']:
        return redirect('dashboard')

    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':

        form = CategoryForm(request.POST, request.FILES, instance=category)

        if form.is_valid():

            form.save()

            messages.success(request, 'Category updated successfully!')

            return redirect('manage_categories')

    else:

        form = CategoryForm(instance=category)

    return render(request, 'dashboard/edit_category.html',
        
        {
            'form': form,
            'category': category,
        }
    )

@login_required
def delete_category(request, category_id):

    if request.user.profile.role not in ['Employee', 'Administrator']:
        
        return redirect('dashboard')

    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':

        category.delete()

        messages.success(request, 'Category deleted successfully!')

        return redirect('manage_categories')

    return render(request, 'dashboard/delete_category.html', {'category': category})

@login_required
def manage_subcategories(request):

    if request.user.profile.role not in ['Employee', 'Administrator']:
        return redirect('dashboard')

    subcategories = (SubCategory.objects.select_related('category').order_by('category__name', 'name'))

    return render(request, 'dashboard/manage_subcategories.html', {'subcategories': subcategories})

@login_required
def add_subcategory(request):

    if request.user.profile.role not in ['Employee', 'Administrator']:
        return redirect('dashboard')

    if request.method == 'POST':

        form = SubCategoryForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            messages.success(request, 'Subcategory added successfully!')

            return redirect('manage_subcategories')

    else:

        form = SubCategoryForm()

    return render(request, 'dashboard/add_subcategory.html', {'form': form})

@login_required
def edit_subcategory(request, subcategory_id):

    if request.user.profile.role not in ['Employee', 'Administrator']:

        return redirect('dashboard')

    subcategory = get_object_or_404(SubCategory, id=subcategory_id)

    if request.method == 'POST':

        form = SubCategoryForm(request.POST, request.FILES, instance=subcategory)

        if form.is_valid():

            form.save()

            messages.success(request, 'Subcategory updated successfully!')

            return redirect('manage_subcategories')

    else:

        form = SubCategoryForm(instance=subcategory)

    return render(request, 'dashboard/edit_subcategory.html',
        
        {
            'form': form,
            'subcategory': subcategory,
        }
    )

@login_required
def delete_subcategory(request, subcategory_id):

    if request.user.profile.role not in ['Employee', 'Administrator']:
        
        return redirect('dashboard')

    subcategory = get_object_or_404(SubCategory, id=subcategory_id)

    if request.method == 'POST':

        subcategory.delete()

        messages.success(request, 'Subcategory deleted successfully!')

        return redirect('manage_subcategories')

    return render(request, 'dashboard/delete_subcategory.html', {'subcategory': subcategory})

@login_required
def manage_reviews(request):

    if request.user.profile.role not in ['Employee', 'Administrator']:
        
        return redirect('dashboard')

    reviews = (Review.objects.select_related('user', 'product').order_by('-date_created'))

    return render(request, 'dashboard/manage_reviews.html', {'reviews': reviews})

@login_required
def edit_review(request, review_id):

    if request.user.profile.role not in ['Employee', 'Administrator']:
        
        return redirect('dashboard')

    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':

        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():

            form.save()

            messages.success(request, 'Review updated successfully!')

            return redirect('manage_reviews')

    else:

        form = ReviewForm(instance=review)

    return render(request, 'dashboard/edit_review.html',
        
        {
            'form': form,
            'review': review,
        },
    )

@login_required
def delete_review(request, review_id):

    if request.user.profile.role not in ['Employee', 'Administrator']:
        
        return redirect('dashboard')

    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':

        review.delete()

        messages.success(request, 'Review deleted successfully!')

        return redirect('manage_reviews')

    return render(request, 'dashboard/delete_review.html', {'review': review})

@login_required
def manage_customers(request):

    if request.user.profile.role != 'Administrator':
        
        return redirect('dashboard')

    customers = (User.objects.filter(profile__role='Customer').select_related('profile').order_by('username'))

    return render(request, 'dashboard/manage_customers.html', {'customers': customers})

@login_required
def customer_details(request, user_id):

    if request.user.profile.role != 'Administrator':
        
        return redirect('dashboard')

    customer = get_object_or_404(User.objects.select_related('profile'), id=user_id, profile__role='Customer')

    purchases = (Purchase.objects.filter(user=customer).order_by('-purchase_date'))

    reviews = (Review.objects.filter(user=customer).select_related('product').order_by('-date_created'))

    return render(request, 'dashboard/customer_details.html',
        
        {
            'customer': customer,
            'purchases': purchases,
            'reviews': reviews,
        },
    )

@login_required
def edit_customer(request, user_id):

    if request.user.profile.role != 'Administrator':
        
        return redirect('dashboard')

    customer = get_object_or_404(User.objects.select_related('profile'), id=user_id, profile__role='Customer')

    if request.method == 'POST':

        form = CustomerEditForm(request.POST, request.FILES, instance=customer.profile)

        if form.is_valid():

            profile = form.save()

            customer.first_name = form.cleaned_data['first_name']
            customer.last_name = form.cleaned_data['last_name']
            customer.email = form.cleaned_data['email']

            customer.save()

            messages.success(request, 'Customer updated successfully!')

            return redirect('customer_details', user_id=customer.id)

    else:

        form = CustomerEditForm(instance=customer.profile)

        form.fields['first_name'].initial = customer.first_name
        form.fields['last_name'].initial = customer.last_name
        form.fields['email'].initial = customer.email

    return render(request, 'dashboard/edit_customer.html',
        
        {
            'form': form,
            'customer': customer,
        },
    )

@login_required
def manage_employees(request):

    if request.user.profile.role != 'Administrator':
        
        return redirect('dashboard')

    employees = (User.objects.filter(profile__role='Employee').select_related('profile').order_by('username'))

    return render(request, 'dashboard/manage_employees.html', {'employees': employees})

@login_required
def add_employee(request):

    if request.user.profile.role != 'Administrator':
        
        return redirect('dashboard')

    if request.method == 'POST':

        form = EmployeeCreationForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            messages.success(request, 'Employee created successfully!')

            return redirect('manage_employees')

    else:

        form = EmployeeCreationForm()

    return render(request, 'dashboard/add_employee.html', {'form': form})

@login_required
def edit_employee(request, user_id):

    if request.user.profile.role != 'Administrator':
        
        return redirect('dashboard')

    employee = get_object_or_404(User.objects.select_related('profile'), id=user_id, profile__role='Employee')

    if request.method == 'POST':

        form = EmployeeEditForm(request.POST, request.FILES, instance=employee.profile)

        if form.is_valid():

            form.save()

            employee.first_name = form.cleaned_data['first_name']
            employee.last_name = form.cleaned_data['last_name']
            employee.email = form.cleaned_data['email']

            employee.save()

            messages.success(request, 'Employee updated successfully!')

            return redirect('manage_employees')

    else:

        form = EmployeeEditForm(instance=employee.profile)

        form.fields['first_name'].initial = employee.first_name
        form.fields['last_name'].initial = employee.last_name
        form.fields['email'].initial = employee.email

    return render(request, 'dashboard/edit_employee.html',
        
        {
            'form': form,
            'employee': employee,
        },
    )