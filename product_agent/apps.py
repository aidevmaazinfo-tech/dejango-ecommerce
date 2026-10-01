from django.apps import AppConfig


class ProductAgentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "product_agent"

    def ready(self):
        import product_agent.signals