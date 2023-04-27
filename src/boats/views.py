from django.views.generic import ListView, DetailView
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from carts.models import Cart
from .models import Boat

# Create your views here.


# class BoatActiveListView(ListView):
#     template_name = "boats/list.html"
#
#     def get_queryset(self, **kwargs):
#         request = self.request
#         return Boat.objects.all().active()
#
#
# class BoatActiveDetailView(DetailView):
#     queryset = Boat.objects.all().active()
#     template_name = "boats/active-detail.html"

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return Product.objects.featured()


class BoatListView(ListView):
    queryset = Boat.objects.all()
    template_name = "boats/list.html"

    def get_queryset(self, **kwargs):
        request = self.request
        return Boat.objects.all()


def boat_list_view(request):
    queryset = Boat.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "boats/list.html", context)


class BoatDetailSlugView(DetailView):
    queryset = Boat.objects.all()
    template_name = "boats/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BoatDetailSlugView, self).get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Boat.objects.get(slug=slug, active=True)
        except Boat.DoesNotExist:
            raise Http404("Not found..")
        except Boat.MultipleObjectsReturned:
            qs = Boat.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        return instance

    def add_to_cart(self, request, slug):

        if request.POST:
            print("POST")

# class BoatDetailView(DetailView):
#     # queryset = Boat.objects.all()
#     template_name = "boats/detail.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(BoatDetailView, self).get_context_data(**kwargs)
#         print(context)
#         return context
#
#     def get_object(self, **kwargs):
#         request = self.request
#         pk = self.kwargs.get('pk')
#         instance = Boat.objects.get_by_id(pk)
#         if instance is None:
#             raise Http404("Product doesn't exist")
#         return instance


def boat_detail_view(request, pk=None, **kwargs):
    #instance = Product.objects.get(pk=pk) #id
    # instance = get_object_or_404(Boat, pk=pk)
    # print(instance)
    instance = Boat.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product doesn't exist")

    context = {
        'object': instance
    }
    return render(request, "boats/detail.html", context)