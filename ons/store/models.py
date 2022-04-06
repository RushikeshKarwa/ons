from distutils.command.upload import upload
from django.db import models
from django.urls import reverse

# Create your models here.
# Model:Category
class Category(models.Model):
    name=models.CharField(max_length=250, unique=True)
    slug=models.SlugField(max_length=250, unique=True)
    description=models.TextField(blank=True)
    image=models.ImageField(upload_to='category', blank=True)

    #to set correct plural for the model changing the name in the db 
    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural='categories'
    
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    #to create human readable formatting
    def __str__(self):
        return self.name

# Model:Product
class Product(models.Model):
    name=models.CharField(max_length=250, unique=True)
    slug=models.SlugField(max_length=250, unique=True)
    description=models.TextField(blank=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='product', blank=True)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    #to set correct plural for the model changing the name in the db 
    class Meta:
        ordering=('name',)
        verbose_name='product'
        verbose_name_plural='products'

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    #to create human readable formatting

    #to dispaly product name
    def __str__(self):
        return self.name

# Model:Cart
class Cart(models.Model):
    cart_id=models.CharField(max_length=250, blank=True)
    date_added= models.DateField(auto_now_add=True)
    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id

#model for the product added to the cart
#many to one relationship to product and cart

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return self.product

# Model:Order

class Order(models.Model):
    token = models.CharField(max_length=250, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='RS Order Total')
    emailAddress = models.EmailField(max_length=250, blank=True, verbose_name='Email Address')
    created = models.DateTimeField(auto_now_add=True)
    billingName = models.CharField(max_length=250, blank=True)
    billingAddress1 = models.CharField(max_length=250, blank=True)
    billingCity = models.CharField(max_length=250, blank=True)
    billingPostcode = models.CharField(max_length=250, blank=True)
    billingCountry = models.CharField(max_length=250, blank=True)
    shippingName = models.CharField(max_length=250, blank=True)
    shippingAddress1 = models.CharField(max_length=250, blank=True)
    shippingCity = models.CharField(max_length=250, blank=True)
    shippingPostcode = models.CharField(max_length=250, blank=True)
    shippingCountry = models.CharField(max_length=250, blank=True)

    class Meta:
        db_table = 'Order'
        ordering = ['-created']

    def __str__(self):
        return str(self.id)
    
class OrderItem(models.Model):
    product = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='RS Price')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = 'OrderItem'

    def sub_total(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product
