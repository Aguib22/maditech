from django.shortcuts import render

from News.models import Actualite

# Create your views here.

def actualite(request):
    
    actualites = Actualite.objects.all()
    context={
        'actualites':actualites
    }

    return render(request, 'News/actualite.html',context)

def detail_actu(request,id):
    new = Actualite.objects.get(pk =id)
    context ={
        'new':new
    }
    
    return render(request,'News/detail_actu.html',context)