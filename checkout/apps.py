from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    def ready(self):
        """
        Override the ready method and import signals module
        Everytime a line item is saved or deleted,
        Custom update total model method will be called.
        Update order totals automatically.
        """
        import checkout.signals
