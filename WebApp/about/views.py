from django.shortcuts import render

from django.contrib.auth.decorators import login_required


# Create your views here. A view is a Python function that takes a web request and returns a web response.
def index(request):
	'''
	@return the display for the about page
	'''
	return render(request, 'about/templates/html/about.html')
