from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

def add_category(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)

			return index(request)
		else:
			print form.errors

	else:
		form = CategoryForm()

	return render(request,'rango/add_category.html',{'form':form})


def add_page(request,category_name_slug):
	try:
		cat = Category.objects.get(category_name_slug)
	except  Category.DoesNotExist:
		cat = None

	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()

				return category(request,category_name_slug)

			else:
				print form.errors
	else:
		form = PageForm()

	context_dict = {'form':form,'category':cat}
	return render(request,'rango/add_page.html',context_dict)




def category(request,category_name_slug):
	context_dict = {}

	try:
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name']= category.name

		pages = Page.objects.filter(category=category)

		context_dict['pages']= pages

		context_dict['category']= category

	except Category.DoesNotExist:

		pass

	return render(request,'rango/category.html',context_dict)

def index(request):
	category_list = Category.objects.order_by('-name')[:5]
	context_dict = {'categories':category_list}
	return render(request,'rango/index.html',context_dict)

def about(request):
	return render(request,'rango/about.html',{})

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username,password=password)

		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect('/rango/')
			else:
				return HttpResponse("your rango account is disabled")

		else:
			print "invalid login details: {0} {1}".format(username,password)
			return HttpResponse("Invalid login details supplied")

	else:
		return render(request,'rango/login.html',{})


@login_required
def restricted(request):
	return HttpResponse("logged in ,you can see the page")


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/rango/')
