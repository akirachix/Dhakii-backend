from django.apps import AppConfig


class CareguideConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'careguide'

    def ready(self):
        pass
