from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from .models import Product
from .forms import ProductModelForm


# Create your views here.
# def bad_view(request, *args, **kwargs):
#     # print(dict(request.GET))
#     my_request_get= dict(request.GET)
#     new_product = my_request_get.get("new_product")
#     print(my_request_get,new_product)
#     if new_product[0].lower()=="true":
#         print("new product")
#         Product.objects.create(title=my_request_get.get("title")[0],content=my_request_get.get("content")[0])
#     return HttpResponse("don't do this")


def search_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello Amit</h1>")
    query=request.GET.get('q')
    qs = Product.objects.filter(title__icontains=query[0])
    print(query,qs)
    context={'name':'rex',"query":query}
    return render(request, "home.html", context)


# def product_create_view(request, *args, **kwargs):
#     print(request.GET)
#     print(request.POST)
#     if request.method=="POST":
#         post_data = request.POST or None
#         if post_data != None :
#             my_form = ProductForm(request.POST)
#             if my_form.is_valid():
#                 print(my_form.cleaned_data.get("title"))
#                 title_from_input = my_form.cleaned_data.get("title")
#                 Product.objects.create(title=title_from_input)
#             # print("post_data", post_data)
#
#     return render(request, "products/forms.html", {})
@staff_member_required()
def product_create_view(request, *args, **kwargs):
    form = ProductModelForm(request.POST or None)
    if form.is_valid() :
        obj=form.save(commit=False)
        #do some stuff
        obj.user = request.user
        obj.save()
        # data=form.cleaned_data
        # Product.objects.create(**data)
        form=ProductModelForm()
    return render(request, "products/forms.html", {"form":form})


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


