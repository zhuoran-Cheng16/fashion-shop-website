from enum import unique
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
class Item(models.Model):
    # Use the default autofield as unique id
    # item_id = models.UUIDField(primary_key=True) 
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    category_gender = models.CharField(max_length = 30)
    category_genre = models.CharField(max_length=30)
    size = models.CharField(max_length=10)
    price = models.FloatField()
    
    
    def __str__(self):
        return 'id=' + str(self.item_id)+" \nName:"+ self.item_name + "\n Description: "+self.description + "\n category_gender: " + self.category_gender + "\n category_genre: "+self.category_genre+ "\n price: " + str(self.price);

class Review(models.Model):
    item  = models.ForeignKey(Item, default=None, on_delete=models.CASCADE)
    creation_time = models.DateTimeField()
    
    nickname = models.CharField(max_length=20)
    review_title = models.CharField(max_length=50)
    review = models.CharField(max_length=500)
    review_picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    rating = models.PositiveSmallIntegerField(choices=(
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),
    ))
    
    class Meta:
            ordering = ['-creation_time',]
    def __str__(self):
        return 'id=' + str(self.review_id) + ", Review by "+ self.nickname+ self.review

class Item_picture(models.Model):
    item = models.ForeignKey(Item, default=None, on_delete=models.CASCADE)
    item_picture = models.FileField(blank=True)
    
    def __str__(self):
        return 'id=' + str(self.item.item_id) +": "+str(self.item_picture)+ ", picture belong by "+ self.item.item_name



class Profile(models.Model):
    bio = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    picture = models.FileField(blank=True)
    def __str__(self):
        return 'id=' + str(self.id) + ',bio="' + self.bio + '"'

class Order(models.Model):
    customer = models.OneToOneField(User, default=None, on_delete=models.PROTECT)
    creation_time = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, default= 123)
    tarcking_num = models.CharField(max_length=100, null=True)
    shipping_price = models.CharField(max_length=50, default=0.0)
    order_total = models.CharField(max_length=100, null=True)
    cupone = models.FloatField(default=1.0)
    @property
    def get_total_price(self):
        order_items = self.orderitem_set.all()
        total_price = sum([item.get_total_price  for item in order_items])
        return total_price
    @property
    def get_total_num(self):
        order_items = self.orderitem_set.all()
        total_num = sum([item.quantity for item in order_items])
        return total_num
    @property
    def get_coupon_value(self):
        original = float(self.get_total_price)
        final = original * (1-self.cupone)
        return final
    @property
    def get_order_total(self):
        original = float(self.get_total_price)
        final = original * self.cupone + float(self.shipping_price)
        return final
        
class OrderItem(models.Model):
    item = models.ForeignKey(Item, default=None, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, default=None, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    selected_size = models.CharField(max_length=30)
    @property
    def get_total_price(self):
        total = self.item.price * self.quantity
        return total 

def LengthValidator(value):
    if value != 10:
        raise ValidationError(
            _('%(value)s is not a valid phone'),
            params={'value': value},
        )

class Address(models.Model):
    customer = models.OneToOneField(User, default=None, on_delete=models.PROTECT)
    fname=models.CharField(max_length=50, default=None)
    lname=models.CharField(max_length=50, default=None)
    country=models.CharField(max_length=50,default=None)
    street_address=models.CharField(max_length=255, default=None)
    city=models.CharField(max_length=20, default=None)
    state=models.CharField(max_length=20,default=None)
    email=models.EmailField(default=None)
    postcode = models.IntegerField(default=None)
    phone_number = models.IntegerField(default=None)
