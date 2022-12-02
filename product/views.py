from django.shortcuts import render
from product.models import Product


def index(request):
    if request.method == 'GET':
        query_key = 'q'
        if query_key in request.GET:
            query = request.GET[query_key]
            if len(query) == 0:
                data = Product.get_all_products()
            else:
                data = Product.filter_name(query)
            return render(request, 'product/products.html', {'products': data})
        return render(request, 'product/products.html', {'products': Product.objects.all()})
