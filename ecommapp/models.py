from django.db import models
from  django.contrib.auth.models import User
# Create your models here.

CATEGORY_CHOICES=(
    ('CR','Curd'),
    ('ML','Milk'),
    ('LS','Lassi'),
    ('MS','Milkshake'),
    ('PN','paneer'),
    ('GH','Ghee'),
    ('CZ','Cheese'),
    ('IC','Ice-creams'),
)

STATE_CHOICES=(('Andhra Pradesh','Andhra Pradesh'),
('Arunachal Pradesh','Arunachal Pradesh'),
('Assam','Assam'),
('Bihar','Bihar'),
('Chhattisgarh','Chhattisgarh'),
('Goa','Goa'),
('Gujarat','Gujarat'),
('Haryana','Haryana'),
('Himachal Pradesh','Himachal Pradesh'),
('Jharkhand','Jharkhand'),
('Karnataka','Karnataka'),
('Kerala','Kerala'),
('Madhya Pradesh','Madhya Pradesh'),
('Maharashtra','Maharashtra'),
('Manipur','Manipur'),
('Meghalaya','Meghalaya'),
('Mizoram','Mizoram'),
('Nagaland','Nagaland'),	
('Odisha','Odisha'),	
('Punjab','Punjab'),
('Rajasthan','Rajasthan'),
('Sikkim','Sikkim'),
('Tamil Nadu','Tamil Nadu'),
('Telangana','Telangana'),
('Tripura','Tripura'),
('Uttar Pradesh','Uttar Pradesh'),
('Uttarakhand','Uttarakhand'),
('West Bengal','West Bengal'),
)

class product(models.Model):
    title=models.CharField(max_length=100)
    Selling_price=models.FloatField()
    discount_price=models.FloatField()
    description =models.TextField()
    composition=models.TextField(default='')
    prodapp=models.TextField(default='')
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='product')
    def __str__(self):
        return self.title
    

class customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    locality=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    mobile=models.IntegerField(default=0)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=50)
    def __str__(self):
        return self.name
    
class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Product=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity * self.Product.discount_price
    
STATE_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delieverd','Delievered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),

)

class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.FloatField()
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=False)

class orderplaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Customer=models.ForeignKey(customer,on_delete=models.CASCADE)
    Product=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    ordered_data=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATE_CHOICES,default='pending')
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,default="")

    @property
    def total_cost(self):
        return self.quantity*self.Product.discount_price

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Product=models.ForeignKey(product,on_delete=models.CASCADE)
