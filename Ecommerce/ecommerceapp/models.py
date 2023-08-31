from django.db import models

# Create your models here.
class Contact(models.Model):
    username=models.CharField(max_length=50)
    email=models.EmailField()
    desc=models.TextField(max_length=500)
    phone_number=models.IntegerField()

    def __str__(self):
        return f"{self.username} - {self.phone_number}"
    
class Product(models.Model):
    prodid=models.AutoField
    prodname=models.CharField(max_length=100)
    prodprice=models.IntegerField(default=0)
    category=models.CharField(max_length=100)
    subcategory=models.CharField(max_length=100)
    desc=models.CharField(max_length=100)

    prodimg=models.ImageField(upload_to='images')

    def __str__(self):
        return f"{self.prodname}"
    

class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    itemList=models.CharField(max_length=5000)
    name=models.CharField(max_length=100)
    address1=models.CharField(max_length=1000)
    address2=models.CharField(max_length=1000)
    email=models.EmailField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pin_code=models.CharField(max_length=100)
    oid=models.CharField(max_length=100)
    totalAmount=models.IntegerField(default=0)
    paid=models.CharField(max_length=500,blank=True,null=True)
    paymentstatus=models.CharField(max_length=100,blank=True)
    phone_number = models.CharField(max_length=100,default="")
    def __str__(self):
        return self.name


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    updated_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)
    delivered=models.BooleanField(default=False)

    def __str__(self):
        return self.updated_desc[0:12] + "..."
