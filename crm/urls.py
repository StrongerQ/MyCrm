from django.conf.urls import url
from crm import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^sale/',views.sale,name='sale_index'),
    url(r'^stu_index/',views.stu_index,name='stu_index'),
]
