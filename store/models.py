from django.db import models

# Create your models here.


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey("Product",on_delete=models.SET_NULL,null=True,related_name='+') # circular dependency
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering =['title']  # default ordering by title


class Promotion(models.Model):
    description  = models.CharField(max_length=255)
    discount = models.FloatField()

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection,on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-inventory']


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = {
        MEMBERSHIP_BRONZE:"BRONZE",
        MEMBERSHIP_SILVER:"SILVER",
        MEMBERSHIP_GOLD:"GOLD"
    }
    
    first_name = models.CharField(max_length=255) 
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['first_name', 'last_name']  # default ordering by first name and last name
# Note: ForeignKey is a one to many relationship, so if you delete the customer, all orders will be deleted



class Order(models.Model):
    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = {
        PAYMENT_STATUS_COMPLETE:"COMPLETE",
        PAYMENT_STATUS_PENDING:"PENDING",
        PAYMENT_STATUS_FAILED:"FAILED"
    }

    placed_at = models.DateField(auto_now_add=True) # first time add the current time
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES,default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveBigIntegerField() # dont store negative values
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)


class Cart(models.Model):
    created_at = models.DateField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True)


