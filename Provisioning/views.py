from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.template import RequestContext, loader
from Provisioning.models import *
from django.utils import timezone

def index(request):

    client = CurrentClientProduct.get_client()
    type_of_product = CurrentClientProduct.get_type_of_product()

    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'all_products': client.product_set.all().filter(type_of_product=type_of_product,
                                                        create_date__gt=timezone.localtime(timezone.now()).date()),
        'client': client,
        'type_of_product': type_of_product
    })

    return StreamingHttpResponse(template.render(context))


def config(request, sn, mac, pdn, swv):
    client = CurrentClientProduct.get_client()
    type_of_product = CurrentClientProduct.get_type_of_product()

    if Product.notexiste(sn, mac):
        p = Product()
        p.create(sn, mac, pdn, swv, client, type_of_product)
        p.save()
    else:
        p = Product.get_product(sn, mac)
        p.counter += 1
        p.save()

    template = loader.get_template(client.folder+'/'+type_of_product.name_config)

    context = RequestContext(request, {})

    return StreamingHttpResponse(template.render(context), content_type="text/xml")


def firmware(request, sn, mac, pdn, swv):
    pass