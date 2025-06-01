
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F,Value,Func,ExpressionWrapper,DecimalField

from django.db.models.functions import Concat
from django.db.models import Count,Sum,Avg,Max,Min
from django.db.models.aggregates import *
from store.models import Customer, Product,OrderItem,Order,Collection,Promotion
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedITem
from django.db import transaction
# Create your views here.

def hello(request):
    # query_set = Product.objects.all() # here objects works like a manager which is interact with the db
    
    # try:
    #     product = Product.objects.get(pk = 0 ) # get the specific product by the get method
    # except ObjectDoesNotExist:
    #     pass 

    exists = Product.objects.filter(pk = 0).exists()
    #keyword = value # Field lookup type for queryset in django doc.
    """
    __gt = greather than 
    __gte = greater than equal
    __lt/__lte = less than or less than equal
    __range = get the ranges value as tuple
    
    """
    
    #queryset = Product.objects.filter(price__range=(20,30)) # filter the price range f20 to 30
    #queryset = Product.objects.filter(collection__id__range=(1,5))
    #queryset = Product.objects.filter(title__icontains ='coffee') # case sensitive icontains
    #queryset = Product.objects.filter(title__icontains = 'coffee')
    # Product.objects.filter(last_update__year = 2020)
    #queryset = Product.objects.filter(description__isnull = True)

    # filter products : inventory < 10 and price < 20 
    # queryset = Product.objects.filter(inventory__lt = 20 , price__lt = 20)
    #instead of passing multple argument we can pass another filter method
    #queryset = Product.objects.filter(inventory__lt = 20).filter(price__lt = 20)
     # filter products : inventory < 10 OR price < 20 using Q object
    # queryset = Product.objects.filter(Q(inventory__lt = 20) | ~Q (price__lt = 20))
    # comapre with a field using F
    #queryset = Product.objects.filter(inventory =F('collection__id'))

    #sorting data
    #queryset = Product.objects.order_by('price','-title').reverse()
    #queryset = Product.objects.order_by('price')[0]
    # queryset = Product.objects.latest('collection_id') # get sinlge object descending order
    # queryset = Product.objects.earliest('price') # get signle ascending order
    # limiting results using slicing
    # queryset = Product.objects.all()[20:30]
    #selecting fields to query
    queryset = Product.objects.values_list('id','title','collection__title')
    # for product in query_set:
    #     print(product)

    """
    Select products that have been ordered
    and sort them by title
    """
    query = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title').reverse()
    order_item = OrderItem.objects.values('product_id').distinct()# get rid of duplicates
    # only and defer method use for selecting specific fields without mentioned fields for defer('field_name') it will not select the field
    #queryset = Product.objects.only('title','price').defer('description') # only select title and price but not description
    return render(request,'hello.html',{"name":"Abid",'products':list(queryset)})
 
def deferringfields(request):
    # defer method is used to not select the field
    queryset = Product.objects.defer('description').all() # it will not select the description field
    return render(request,'another.html',{"name":"Abid",'products':list(queryset)})

def select_related(request):
    # select related is used to select the related fields prefetching the data
    # it will not hit the db again for the related field
    #prefetch is used for many to many relationship
    queryset = Product.objects.select_related('collection').all() # it will select the collection field
    queryset2 = Product.objects.prefetch_related('promotions').select_related('collection').all() 
    return render(request,'another.html',{"name":"Abid",'products':queryset2})

def orders(request):
   #Get the last 5 orders with their customer and items include products

    queryset2 =Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('placed_at').all()
    
    return render(request,'another.html',{"name":"Abid",'orders':queryset2})

def aggregate_used(request):
    # aggregate is used to perform aggregation on the queryset
    # queryset2 = Order.objects.aggregate(
    #     total_orders=Count('id'),
    #     total_customers=Count('customer_id',distinct=True),
    #     total_items=Sum('orderitem__quantity'),
    #     total_price=Sum(F('orderitem__product__price') * F('orderitem__quantity'))
    # )
   
   result =  Product.objects.filter(inventory__gt = 70).aggregate(count = Count('id'),min_price= Min('price'),max_price=Max('price'),avg_price=Avg('price'),sum_price=Sum('price'))
   return render(request,'counting.html',{"name":"Abid",'result':result})

def annonate(request):
    #Google it to know more about Django database functions
    # annotate is used to add a new field to the queryset
    # it will not hit the db again for the related field
    queryset = Product.objects.annotate(new_id = F('id') + 10)
    queryset2 = Customer.objects.annotate(
        #CONCAT the strings together
        full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
    )
    queryset3 = Customer.objects.annotate(
        #CONCAT the strings together
        full_name=Concat('first_name',Value(' '),'last_name'))
    
    queryset4 = Customer.objects.annotate(
        orders_count=Count('order')
    )
    discounted_price = ExpressionWrapper(F('price')*0.8,output_field=DecimalField())
    queryset5 = Product.objects.annotate(
        discounted_price = discounted_price
    )

    queryset6 = TaggedITem.objects.get_tags_for(Product,1) # get the tags for the product with id 1
    #insert a new record int the collection table
    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Product(pk = 1) # get the first product
    # collection.save() # save the collection to the db
    #another approach to insert a new record in the collection table
    # Collection.objects.create(title='Video Games',featured_product=Product(pk=1))
   
    #UPDATE THE COLLECTION OBJECT
    # collection = Collection(pk=11) # get the collection with id 1
    # collection.title = 'Games Play'
    # # collection.featured_product =None 
    # collection.save() # save the collection to the db
    #only update the collection id 13 with featured product = None
    # Collection.objects.filter(id=13).update(title = 'MUSIC',featured_product=None)
    # #delete the collection with id greater than 10
    # Collection.objects.filter(id__gt=10).delete()

    #tranaction management for order and item

    with transaction.atomic():
        order = Order.objects.create(customer=Customer(pk=1),payment_status='P')
        OrderItem.objects.create(order=order,product=Product(pk=1),quantity=2,unit_price = 10)
       




    return render(request,'counting.html',{"name":"Abid",'products':list(queryset6)})

    











    