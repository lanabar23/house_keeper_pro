from django.shortcuts import render

# Create your views here.
def hub_view(request):
    return render(request, 'house_keeper_hub.html')

