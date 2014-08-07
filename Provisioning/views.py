from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.template import RequestContext, loader
from Provisioning.models import Product

# Create your views here.
#test

titi = "titi"

def index(request,):
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'all_products': Product.objects.all(),
        'titi': titi
    })
    return StreamingHttpResponse(template.render(context))

def config(request, sn, mac, pdn, swv):
    titi = "Truc"
    p = Product()
    p.init(sn, mac, pdn, swv)
    p.save()
    template = loader.get_template('WRP400.xml')
    context = RequestContext(request, {
#        'latest_poll_list': latest_poll_list,
    })
    return StreamingHttpResponse(template.render(context))

def firmware(request, sn, mac, pdn, swv):
    pass