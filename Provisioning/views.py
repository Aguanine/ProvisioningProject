from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.template import RequestContext, loader
from Provisioning.models import *
from django.utils import timezone

# Create your views here.

def index(request,):
    current_client_product = CurrentClientProduct.objects.all()[0].current_client_product

    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'all_products': current_client_product.client.product_set.all().filter(type_of_product=current_client_product.type_of_product,
                                                                               create_date__gt=timezone.localtime(timezone.now()).date()),
        'client': current_client_product.client,
        'type_of_product': current_client_product.type_of_product
    })
    return StreamingHttpResponse(template.render(context))


def config(request, sn, mac, pdn, swv):
    current_client_product = CurrentClientProduct.objects.all()[0].current_client_product

    client = current_client_product.client
    type_of_product = current_client_product.type_of_product

    listProd = client.product_set.all().filter(mac=mac, serial_number=sn)

    if not listProd:
        p = Product()
        p.create(sn, mac, pdn, swv, client, type_of_product)
        p.save()
    else:
        p = listProd[0]
        p.counter += 1
        p.save()

    template = loader.get_template(client.folder+'/'+type_of_product.name_config)

    context = RequestContext(request, {})

    return StreamingHttpResponse(template.render(context), content_type="text/xml")


def firmware(request, sn, mac, pdn, swv):
    pass