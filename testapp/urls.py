from django.urls import path
from . import views

urlpatterns =[

    path('hello/',views.hello), 
    path('defer/', views.deferringfields),
    path('select/', views.select_related),
    path('orders/', views.orders),
    path('agg/', views.aggregate_used),
    path('annotate/', views.annonate),
]