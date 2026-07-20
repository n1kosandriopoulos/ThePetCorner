from django import forms
from .models import Product, Category, SubCategory


class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = '__all__'

        widgets = {

            'subcategory': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'product_code': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'brand': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                }
            ),

            'price': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),

            'stock_quantity': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),

            'image': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),

        }

class CategoryForm(forms.ModelForm):

    class Meta:

        model = Category

        fields = '__all__'

        widgets = {

            'name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                }
            ),

        }

class SubCategoryForm(forms.ModelForm):

    class Meta:

        model = SubCategory

        fields = '__all__'

        widgets = {

            'category': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                }
            ),

            'image': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),

        }