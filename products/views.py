from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from .models import Product


# Create your views here.
def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello Amit</h1>")
    context={'name':'rex'}
    return render(request, "home.html", context)


def product_detail_view(request, pk, *args, **kwargs):
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise Http404
    # return HttpResponse(f"product id {obj.pk}")
    return render(request, "products/detail.html", {"object": obj})


def product_list_view(request, *args, **kwargs):
    qs = Product.objects.all()
    context = {"object_list": qs}
    return render(request, "products/list.html", context)


def product_api_detail_view(request, pk, *args, **kwargs):
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({"id": "not found"})
    return JsonResponse({"id": obj.pk})


