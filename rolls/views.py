from django.shortcuts import get_object_or_404,  render

from .models import RollType
# Create your views here.
def index(request):
  rollTypes = RollType.objects.order_by('name')[:5]
  context = {'rollTypes': rollTypes}
  return render(request, 'rolls/index.html', context)

def detail(request, roll_id):
    roll = get_object_or_404(RollType, pk=roll_id)
    return render(request, 'rolls/detail.html', {'roll' : roll})