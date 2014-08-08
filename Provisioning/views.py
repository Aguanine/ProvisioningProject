from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.template import RequestContext, loader
from Provisioning.models import *

# Create your views here.

def index(request,):
    current_client = CurrentClient.objects.all()[0].current_client

    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'all_products': current_client.product_set.all(),
        'current_client': current_client,
        'type_of_product': current_client.type_of_products.all()
    })
    return StreamingHttpResponse(template.render(context))

def config(request, sn, mac, pdn, swv):
    current_client = CurrentClient.objects.all()[0].current_client

    # TEST
    tp1 = TypeOfProduct.objects.all()[0]

    p = Product()
    p.create(sn, mac, pdn, swv, current_client, tp1)
    p.save()
    template = loader.get_template('WRP400.xml')
    context = RequestContext(request, {
#        'latest_poll_list': latest_poll_list,
    })
    return StreamingHttpResponse(template.render(context))

def firmware(request, sn, mac, pdn, swv):
    pass