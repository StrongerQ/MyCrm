from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return render(request,'index.html')

def sale(request):
    return render(request,'sale_index.html')

def stu_index(request):
    return render(request,'stu_index.html')