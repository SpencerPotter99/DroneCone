from django.apps import AppConfig


class DronecustomerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DroneCustomer'

    def ready(self):
        import DroneCustomer.signals  # noqa