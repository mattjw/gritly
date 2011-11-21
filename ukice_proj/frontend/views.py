# Create your views here.
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template 

@requires_csrf_token
def index(request):
	return direct_to_template( request, template='index.html' )