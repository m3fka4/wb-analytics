from django.shortcuts import render
from .models import Product
from .forms import ProductFilterForm

def product_list(request):
    form = ProductFilterForm(request.GET or None)
    qs = Product.objects.all()
    if form.is_valid():
        cd = form.cleaned_data
        if cd['min_price'] is not None:
            qs = qs.filter(price__gte=cd['min_price'])
        if cd['max_price'] is not None:
            qs = qs.filter(price__lte=cd['max_price'])
        if cd['min_rating'] is not None:
            qs = qs.filter(rating__gte=cd['min_rating'])
        if cd['min_reviews'] is not None:
            qs = qs.filter(reviews_count__gte=cd['min_reviews'])
    return render(request, 'analytics/product_list.html', {
        'form': form,
        'products': qs
    })