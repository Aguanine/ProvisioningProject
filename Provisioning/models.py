from django.db import models
from django.utils import timezone

# Create your models here.

# class Poll(models.Model):
    # question = models.CharField(max_length=200)
    # pub_date = models.DateTimeField('date published')
# 
# class Choice(models.Model):
    # poll = models.ForeignKey(Poll)
    # choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    software_version = models.CharField(max_length=200)
    mac = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=200)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(auto_now=True)
    
    def __init__(self, *args, **kwargs) :
        super(Product, self).__init__(*args, **kwargs)
    
    def init(self, serial_number, mac, product_name, software_version) :
        self.product_name = product_name
        self.software_version = software_version
        self.mac = mac
        self.serial_number = serial_number
        self.create_date = timezone.now()
        self.update_date = timezone.now()
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return "Product Name : %s ; Software Version : %s ; MAC : %s ; Serial Number : %s ; Date Creation : %s ; Date Update : %s" % (self.product_name, self.software_version, self.mac, self.serial_number, self.create_date, self.update_date)
    
    def __str__(self):
        return "Product Name : %s ; Software Version : %s ; MAC : %s ; Serial Number : %s ; Date Creation : %s ; Date Update : %s" % (self.product_name, self.software_version, self.mac, self.serial_number, self.create_date, self.update_date)
        

class Client(models.Model):
    Name = models.CharField(max_length=200)


class TypeProduct(models.Model):
    label = models.CharField(max_length=200)
    pass


class ConfigProduct(models.Model):
    pass
    
class CurentClient(models.Model):
    pass
    