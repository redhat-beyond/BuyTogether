from django.shortcuts import render
from .. import models


def index(request):
    if request.method == 'GET':
        query_key = 'q'
        if query_key in request.GET:
            query = request.GET[query_key]
            if len(query) == 0:
                data = models.Product.get_all_products()
            else:
                models.Product.filter_name(query)
            return render(request, 'buy_together_app/products.html', {'products': data})
        return render(request, 'buy_together_app/products.html', {'products': models.Product.objects.all()})
