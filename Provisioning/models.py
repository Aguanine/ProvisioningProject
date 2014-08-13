from django.db import models
from django.utils import timezone


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    software_version = models.CharField(max_length=200)
    mac = models.CharField(max_length=200, unique=True)
    serial_number = models.CharField(max_length=200, unique=True)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(auto_now=True)
    counter = models.IntegerField()
    client = models.ForeignKey("Client")
    type_of_product = models.ForeignKey("TypeOfProduct")

    @classmethod
    def notexiste(cls, serial_number, mac):
        if not Product.objects.all().filter(serial_number=serial_number, mac=mac):
            return True
        else:
            return False

    @classmethod
    def get_product(cls, serial_number, mac):
        return Product.objects.all().filter(serial_number=serial_number, mac=mac)[0]

    def create(self, serial_number, mac, product_name, software_version, client, type_of_product):
        self.product_name = product_name
        self.software_version = software_version
        self.mac = mac
        self.serial_number = serial_number
        self.client = client
        self.type_of_product = type_of_product
        self.create_date = timezone.now()
        self.update_date = timezone.now()
        self.counter = 1


    def __unicode__(self):
        return u'Type Of Product : %s ; ' \
               u'Product Name : %s ; ' \
               u'Software Version : %s ; ' \
               u'MAC : %s ; ' \
               u'Serial Number : %s ; ' \
               u'Client : %s ; ' \
               u'Count : %s ; ' \
               u'Date Creation : %s ; ' \
               u'Date Update : %s' % (self.type_of_product,
                                      self.product_name,
                                      self.software_version,
                                      self.mac,
                                      self.serial_number,
                                      self.client,
                                      self.counter,
                                      self.create_date,
                                      self.update_date)



class Client(models.Model):
    name = models.CharField(max_length=200, unique=True)
    folder = models.CharField(max_length=200, unique=True)
    type_of_products = models.ManyToManyField("TypeOfProduct")

    def __unicode__(self):
        return u'%s' % self.name



class TypeOfProduct(models.Model):
    label = models.CharField(max_length=200, unique=True)
    name_config = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return u'%s' % self.label



class ConfigProduct(models.Model):
    client = models.ForeignKey("Client")
    type_of_product = models.ForeignKey("TypeOfProduct")

    def __unicode__(self):
        return u'%s -> %s' % (self.client, self.type_of_product)

    class Meta:
        unique_together = ("client", "type_of_product")



class CurrentClientProduct(models.Model):
    current_client_product = models.ForeignKey("ConfigProduct", unique=True)

    @classmethod
    def get_client(cls):
        current_client_product = CurrentClientProduct.objects.all()[0].current_client_product
        return current_client_product.client

    @classmethod
    def get_type_of_product(cls):
        current_client_product = CurrentClientProduct.objects.all()[0].current_client_product
        return  current_client_product.type_of_product
