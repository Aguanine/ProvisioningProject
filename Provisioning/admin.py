from django.contrib import admin
from Provisioning.models import Product, Client, TypeOfProduct, ConfigProduct, CurrentClient

admin.site.register(Product)

admin.site.register(Client)

admin.site.register(TypeOfProduct)

admin.site.register(ConfigProduct)

admin.site.register(CurrentClient)