import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, 
                                     related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        # generate a random string of 32 characters to use as order no.
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs
        """

        # use sum function accross all lineitem total fields
        # add new field to query 'lineitem_total__sum'
        # set the order total to that
        # 'or 0' prevents error if line item is manually deleted
        #   order total is '0' not 'none'
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        # calculate the delivery cost
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            # 0 if order is higher than threshold
            self.delivery_cost = 0

        # calculate grand total
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        If it hasn't been set already
        """

        # generate new order no. if none already
        if not self.order_number:
            self.order_number = self._generate_order_number()

        # execute original save method
        super().save(*args, **kwargs)

    def __str__(self):
        # string to return order number
        return self.order_number


class OrderLineItem(models.Model):
    """
    Use the info the user entered in the payment form to create order instance
    Iterate throuhg the items in the shopping bag
    Create an orderline item for each one
    Attach it to the order
    Update the delivery cost, order total and grand total along the way
    """
    # ForeignKey to the order, related name of line items
    # allowing access to order and make calls from it (order.lineitems.all)
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False,
                                on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True,
                                    blank=True)  # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, blank=False,
                                         editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the line item total
        and update the order total
        """

        self.lineitem_total = self.product.price * self.quantity

        # execute original save method
        super().save(*args, **kwargs)

    def __str__(self):
        # string to return SKU of the product
        return f'SKU {self.product.sku} on order {self.order.order_number}'
