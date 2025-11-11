from django.apps import AppConfig

class EcoenAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Prog_EcoEn.ecoen_app'

def ready(self):
    import Prog_EcoEn.ecoen_app.signals  # ajustá el path si usás otro nombre