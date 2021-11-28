from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe
# Create your models here.

# Customer Model 
CITY_CHOICES = (
    ('Dhaka', 'Dhaka'),
    ('Chittagong', 'Chittagong'),
)
AREA_CHOICES = (
    ('Bashundhara', 'Bashundhara'),
    ('Gulshan', 'Gulshan'),
    ('Mirpur', 'Mirpur'),
    ('Banani', 'Banani'),
    ('Uttara', 'Uttara'),
    ('Wari', 'Wari'),
    ('Jatrabri', 'Jatrabri'),
    ('Gulishtan', 'Gulishtan'),
    ('Khulshi', 'Khulshi'),
    ('GEC', 'GEC'),
    ('Lalkhan Bazar', 'Lalkhan Bazar'),
    ('Dewan Hat', 'Dewan Hat'),
    ('Agrabad', 'Agrabad'),
    ('2no Gate', '2no Gate'),
    ('Muradpur', 'Muradpur'),
    ('Bahaddarhat', 'Bahaddarhat'),
    ('Wasa', 'Wasa'),
    ('Katghar', 'Katghar'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=50)
    address = models.TextField()
    city = models.CharField(choices=CITY_CHOICES, max_length=50)
    area = models.CharField(choices=AREA_CHOICES, max_length=50)
    zipcode = models.IntegerField()


    def __str__(self):
        return self.name+' '+'(ID: 70'+str(self.id)+')'

# Product Models

CATEGORY_CHOICES = (
    ('Grocery', 'Grocery'),
    ('Rice', 'Rice'),
    ('Fish', 'Fish'),
    ('Oil', 'Oil'),
    ('Vegetables', 'Vegetables'),
    ('Beverages', 'Beverages'),
    ('Meat', 'Meat'),
    ('Bakery & Snacks', 'Bakery & Snacks'),
    ('Dairy', 'Dairy'),
    ('Household & Clean', 'Household & Clean'),
)

class Product(models.Model):
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    product_name = models.CharField(max_length=200)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    product_description = models.TextField()
    brand = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='product/')
    offer = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name+' '+'(Product ID: 30'+str(self.id)+')'    


    def imageurl(self):
        if self.photo:
            return self.photo.url
        else:
            return ""

    def image_tag(self):
        return mark_safe('<img src="{}" heights="80" width="60" />'.format(self.photo.url)) 
    image_tag.short_description = 'Photo'

# Cart Models 

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property 
    def total_cost(self):
        return self.quantity * self.product.discounted_price

# Order Models 
STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),

)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)    
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, default='Pending', max_length=50)    


    @property 
    def total_cost(self):
        return self.quantity * self.product.discounted_price


        
class Banner(models.Model):
    image = models.ImageField(upload_to='banner/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def imageurl(self):
        if self.image:
            return self.image.url
        else:
            return ""

    def image_tag(self):
        return mark_safe('<img src="{}" heights="80" width="60" />'.format(self.image.url)) 
    image_tag.short_description = 'image'
