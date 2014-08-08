from django.db import models
from django.utils import timezone


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    software_version = models.CharField(max_length=200)
    mac = models.CharField(max_length=200, unique=True)
    serial_number = models.CharField(max_length=200, unique=True)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(auto_now=True)
    client = models.ForeignKey("Client")
    type_of_product = models.ForeignKey("TypeOfProduct")

    def create(self, serial_number, mac, product_name, software_version, client, type_of_product):
        self.product_name = product_name
        self.software_version = software_version
        self.mac = mac
        self.serial_number = serial_number
        self.client = client
        self.type_of_product = type_of_product
        self.create_date = timezone.now()
        self.update_date = timezone.now()

    def __unicode__(self):
        return u'Product Name : %s ; ' \
               u'Software Version : %s ; ' \
               u'MAC : %s ; ' \
               u'Serial Number : %s ; ' \
               u'Date Creation : %s ; ' \
               u'Date Update : %s' % (self.product_name,
                                      self.software_version,
                                      self.mac,
                                      self.serial_number,
                                      self.create_date,
                                      self.update_date)



class Client(models.Model):
    name = models.CharField(max_length=200, unique=True)
    type_of_products = models.ManyToManyField("TypeOfProduct")

    def __unicode__(self):
        return u'Name of client : %s' % self.name



class TypeOfProduct(models.Model):
    label = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return u'Type of product : %s' % self.label



class ConfigProduct(models.Model):
    name_config = models.CharField(max_length=200, unique=True)
    client = models.ForeignKey("Client")
    type_of_product = models.ForeignKey("TypeOfProduct")

    def __unicode__(self):
        return u'Name of config : %s' % self.name_config

    class Meta:
        unique_together = ("client", "type_of_product")



class CurrentClient(models.Model):
    current_client = models.ForeignKey("Client", unique=True)
