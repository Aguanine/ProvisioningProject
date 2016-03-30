from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseNotFound
from django.template import RequestContext, loader
from Provisioning.models import *
from django.utils import timezone
from django.forms import ModelForm
import csv
import os
import datetime
from django.utils import timezone
from django import forms


class CurrentClientProductForm(forms.Form):
    current_client_product = forms.ModelChoiceField(queryset=ConfigProduct.objects.all())
    start_date = forms.SplitDateTimeField(input_date_formats=['%d/%m/%Y'], input_time_formats=['%H:%M:%S'], required=False, initial=CurrentClientProduct.get_start_date())

def index(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = CurrentClientProductForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            ccp = CurrentClientProduct.objects.all()[0]
            ccpForm = form.cleaned_data['current_client_product']
            sdForm = form.cleaned_data['start_date']
            ccp.current_client_product = ccpForm
            ccp.start_date = sdForm
            ccp.save()

    client = CurrentClientProduct.get_client()
    type_of_product = CurrentClientProduct.get_type_of_product()
    firm = CurrentClientProduct.get_firmware()
    all_products = client.product_set.all().filter(type_of_product=type_of_product, create_date__gt=CurrentClientProduct.get_start_date())
    contact_form = CurrentClientProductForm()
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'all_products': all_products,
        'firmware': firm,
        'client': client,
        'type_of_product': type_of_product,
        'contact_form': contact_form
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

def configok(request, sn, mac, pdn, hwv, swv):
    client = CurrentClientProduct.get_client()
    type_of_product = CurrentClientProduct.get_type_of_product()
    p = Product.get_product(sn, mac)
    p.provok(True)
    p.save()
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

    all_products = client.product_set.all().filter(type_of_product=type_of_product, create_date__gt=CurrentClientProduct.get_start_date())\
        #,create_date__gt=timezone.localtime(timezone.now()).date())

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    attachement = u'attachment; filename="Export-%s-%s.csv"' % (client.name, timezone.localtime(timezone.now()).date())
    response['Content-Disposition'] = attachement

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Type Of Product','Product Name','Hardware Version','Software Version','MAC','Serial Number','Client','Count','Date Creation','Date Update','Provisioning Status'])
    for x in all_products:
        #if x.isupdate and x.counter == 1:
        writer.writerow([x.type_of_product,x.product_name,x.hardware_version,x.software_version,x.mac,x.serial_number,x.client,x.counter,x.create_date,x.update_date,x.provok])

    return response

