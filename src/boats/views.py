from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from .models import Boat

# Create your views here.

class BoatListView(ListView):
    queryset = Boat.objects.all()
    template_name = "boats/list.html"

    def get_context_data(self, **kwargs):
        context = super(BoatListView, self).get_context_data(**kwargs)
        print(context)
        return context


def boat_list_view(request):
    queryset = Boat.objects.all()
    context = {
        'qs': queryset
    }
    return render(request, "boats/list.html", context)


class BoatDetailView(DetailView):
    queryset = Boat.objects.all()
    template_name = "boats/detail.html"

    def get_context_data(self, **kwargs):
        context = super(BoatDetailView, self).get_context_data(**kwargs)
        print(context)
        # context['abc'] = 123
        return context


def Boat_detail_view(request, pk=None, **kwargs):
    #instance = Product.objects.get(pk=pk) #id
    instance = get_object_or_404(Boat, pk=pk)
    print(instance)
    context = {
        'object': instance
    }
    return render(request, "boats/detail.html", context)