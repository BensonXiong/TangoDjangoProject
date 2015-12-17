from django.shortcuts import render

# Create your views here.
def index(request):
	context={'boldmessage':'I am bold ont from the context'}
	return render(request,'rango/index.html',context)