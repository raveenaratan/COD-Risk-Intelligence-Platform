from django.db import models


class Order(models.Model):
    order_id = models.CharField(max_length=50)
    order_datetime = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)

    order_value = models.FloatField()

    items = models.TextField()

    num_items = models.IntegerField(default=0)
    customer_prior_orders = models.IntegerField(default=0)
    customer_prior_rto = models.IntegerField(default=0)

    utm_source = models.CharField(max_length=100)

    courier = models.CharField(max_length=100)

    payment_method = models.CharField(max_length=50)

    final_status = models.CharField(max_length=50)

    def __str__(self):
        return self.order_id

# Create your models here.
