from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Handle signals from post_save event:
        - Sender of the signal
        - Acutal instance of the model that sent it
        - Boolean sent by Django for either update/create
        - Keyword arguements

    Update order total on lineitem update/create
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.order.update_total()
