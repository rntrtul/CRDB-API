from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count
from rest_framework.pagination import PageNumberPagination

from .models import Rolls, RollType, Advantage, AdvantageType, Kill, Die
from .serializers import RollsSerializer, RollTypeSerializer, RollTypeDetailSerializer, AdvantageSerializer, \
    AdvantageTypeSerializer, KillSerializer, DieSerializer, RankingSerializer
from rest_framework import generics, viewsets
from rest_framework import filters as rf_filters
from django_filters import rest_framework as filters


# Create your views here.
# REST views
class RollFilter(filters.FilterSet):
    min_nat_value = filters.NumberFilter(field_name="natural_value", lookup_expr='gte')
    max_nat_value = filters.NumberFilter(field_name="natural_value", lookup_expr='lte')
    min_final_value = filters.NumberFilter(field_name="final_value", lookup_expr='gte')
    max_final_value = filters.NumberFilter(field_name="final_value", lookup_expr='lte')
    episode_start = filters.NumberFilter(field_name="ep__num", lookup_expr='gte')
    episode_end = filters.NumberFilter(field_name="ep__num", lookup_expr='lte')
    min_timestamp = filters.NumberFilter(field_name="time_tamp", lookup_expr='gte')
    max_timestamp = filters.NumberFilter(field_name="timestamp", lookup_expr='lte')
    min_kills = filters.NumberFilter(field_name="kill_count", lookup_expr='gte')
    max_kills = filters.NumberFilter(field_name="kill_count", lookup_expr='lte')

    class Meta:
        model = Rolls
        fields = ['character', 'ep', 'roll_type', 'kill_count',
                  'min_nat_value', 'max_nat_value', 'min_final_value', 'max_final_value', 'episode_start',
                  'episode_end',
                  'min_timestamp', 'max_timestamp', 'min_kills', 'max_kills']


class StandardRollsPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 1000


class RollsViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Rolls.objects.order_by('ep__campaign', 'ep__num', 'timestamp')
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    filterset_class = RollFilter
    serializer_class = RollsSerializer
    pagination_class = StandardRollsPagination


class RollTypeViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'list':
            return RollTypeSerializer
        else:
            return RollTypeDetailSerializer

    def get_queryset(self):
        queryset = RollType.objects.all()
        if self.action == list:
            queryset = self.get_serializer_class().setup_eager_loading(queryset)

        return queryset


class AdvantageTypeViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.action == 'list':
            return AdvantageType.objects.order_by('name')
        return AdvantageType.objects.all()

    serializer_class = AdvantageTypeSerializer


class AdvantageViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.action == 'list':
            return Advantage.objects.order_by('used__ep')
        return Advantage.objects.all()

    serializer_class = AdvantageSerializer


class KillViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.action == 'list':
            return Kill.objects.order_by('-count', 'roll')
        return Kill.objects.all()

    serializer_class = KillSerializer


class DieViewSet(viewsets.ModelViewSet):
    queryset = Die.objects.order_by('sides')
    serializer_class = DieSerializer


class RankingViewSet(viewsets.ModelViewSet):
    queryset = Rolls.objects.all()[0:1]
    serializer_class = RankingSerializer

# django template views
class IndexView(generic.ListView):
    template_name = 'rolls/index.html'
    context_object_name = 'rolls_list'
    paginate_by = 100

    def get_queryset(self):
        return Rolls.objects.order_by('ep', 'timestamp')  # only get first 100 otherwise too many


class DetailView(generic.DetailView):
    model = Rolls
    template_name = 'rolls/detail.html'


class TypeListView(generic.ListView):
    template_name = 'rolls/typeIndex.html'
    context_object_name = 'type_list'

    def get_queryset(self):
        return RollType.objects.annotate(num_rolls=Count('rolls')).order_by('-num_rolls')


class TypeDetailView(generic.DetailView):
    model = RollType
    template_name = 'rolls/typeDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roll_list'] = context['object'].rolls.order_by('ep__num', 'timestamp')[:100]
        context['c1_count'] = context['object'].rolls.filter(ep__campaign_id=5).count()
        context['c2_count'] = context['object'].rolls.filter(ep__campaign_id=6).count()
        return context
