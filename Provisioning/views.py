from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseNotFound
from django.template import RequestContext, loader
from Provisioning.models import *
from django.utils import timezone
import csv
import os
import datetime


def index(request):
    client = CurrentClientProduct.get_client()
    type_of_product = CurrentClientProduct.get_type_of_product()
    firm = CurrentClientProduct.get_firmware()
    all_products = client.product_set.all().filter(type_of_product=type_of_product, create_date__gt=timezone.localtime(timezone.now()).date() - datetime.timedelta(days=1))

    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'all_products': all_products,
        'firmware': firm,
        'client': client,
        'type_of_product': type_of_product
    })

    return StreamingHttpResponse(template.render(context))


def config(request, sn, mac, pdn, hwv, swv):
    client = CurrentClientProduct.get_client()
    type_of_product = CurrentClientProduct.get_type_of_product()

    if Product.notexiste(sn, mac):
        p = Product()
        p.create(sn, mac, pdn, hwv, swv, client, type_of_product)
        p.save()
    else:
        p = Product.get_product(sn, mac)
        p.update_isupdate(swv)
        p.save()

    if p.isupdate:
        p.counter += 1
        p.save()
        template = loader.get_template(client.folder+'/'+type_of_product.name_config)
        context = RequestContext(request, {})
        return StreamingHttpResponse(template.render(context), content_type="text/xml")

    return StreamingHttpResponse("", content_type="text/xml")

def firmware(request, sn, mac, pdn, hwv, swv):
    client = CurrentClientProduct.get_client()
    type_of_product = CurrentClientProduct.get_type_of_product()

    if Product.notexiste(sn, mac):
        p = Product()
        p.create(sn, mac, pdn, hwv, swv, client, type_of_product)
        p.save()
    else:
        p = Product.get_product(sn, mac)
        p.update_isupdate(swv)
        p.save()

    if CurrentClientProduct.get_name_firmware() == "":
        return HttpResponseNotFound()

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))+'/Provisioning/templates'
    file_data = open(BASE_DIR+'/'+client.folder+'/'+CurrentClientProduct.get_name_firmware(), "rb").read()
    response = HttpResponse(file_data)
    response['Content-Disposition'] = 'attachment; filename='+CurrentClientProduct.get_name_firmware()
    return response

def export(request):
    client = CurrentClientProduct.get_client()
    type_of_product = CurrentClientProduct.get_type_of_product()

    all_products = client.product_set.all().filter(type_of_product=type_of_product)\
        #,create_date__gt=timezone.localtime(timezone.now()).date())

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    attachement = u'attachment; filename="Export-%s-%s.csv"' % (client.name, timezone.localtime(timezone.now()).date())
    response['Content-Disposition'] = attachement

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Type Of Product','Product Name','Hardware Version','Software Version','MAC','Serial Number','Client','Count','Date Creation','Date Update'])
    for x in all_products:
        #if x.isupdate and x.counter == 1:
        writer.writerow([x.type_of_product,x.product_name,x.hardware_version,x.software_version,x.mac,x.serial_number,x.client,x.counter,x.create_date,x.update_date])

    return response

