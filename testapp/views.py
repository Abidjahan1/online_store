from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F
from store.models import Product,OrderItem
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
    return render(request,'hello.html',{"name":"Abid",'products':list(query)})
 
