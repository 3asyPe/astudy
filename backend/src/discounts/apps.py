from django.apps import AppConfig


class DiscountsConfig(AppConfig):
    name = 'discounts'

    def ready(self):
      import discounts.signals
