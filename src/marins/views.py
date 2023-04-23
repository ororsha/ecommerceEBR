from django.views.generic import ListView, DetailView
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Marin

# Create your views here.


class MarinListView(ListView):
    queryset = Marin.objects.all()
    template_name = "marins/list.html"

    def get_queryset(self, **kwargs):
        request = self.request
        return Marin.objects.all()


def marin_list_view(request):
    queryset = Marin.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "marins/list.html", context)


class MarinDetailSlugView(DetailView):
    queryset = Marin.objects.all()
    template_name = "marins/detail.html"

    def get_context_data(self, **kwargs):
        context = super(MarinDetailSlugView, self).get_context_data(**kwargs)
        return context

    def get_object(self, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Marin.objects.get(slug=slug, active=True)
        except Marin.DoesNotExist:
            raise Http404("Not found..")
        except Marin.MultipleObjectsReturned:
            qs = Marin.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        return instance