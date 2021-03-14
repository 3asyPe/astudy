from django.apps import AppConfig


class CartsConfig(AppConfig):
    name = 'carts'

    def ready(self):
      import carts.signals

