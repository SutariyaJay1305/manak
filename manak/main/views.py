from django.shortcuts import render

from .models import UIManager,DataManager

# Create your views here.

def index(request):
    text1 = UIManager.objects.get(UI_position=1).text_description
    text2 = UIManager.objects.get(UI_position=2).text_description
    context = {
        "text1":text1,
        "text2":text2,
        
        }
    
    return render(request,'index.html',context)


def report(request):
    data = DataManager.objects.all()
    print(data)
    
    return render(request,'report.html',{"data":data})