from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from boats.models import Boat
from marins.models import Marin

# Create your views here.


class SearchBoatView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, **kwargs):
        context = super(SearchBoatView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        # SearchQuery.objects.create(query=query)
        return context

    def get_queryset(self, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None) # method_dict['q']
        # print(query)
        if query is not None:
            lookups = Q(boat_category__icontains=query) | Q(description__icontains=query) | Q(title__icontains=query)
            return Boat.objects.search(query)
        return Boat.objects.active()


class SearchMarinView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, **kwargs):
        context = super(SearchMarinView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        # SearchQuery.objects.create(query=query)
        return context

    def get_queryset(self, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None) # method_dict['q']
        # print(query)
        if query is not None:
            lookups = Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
            return Marin.objects.search(query)
        return Marin.objects.active()