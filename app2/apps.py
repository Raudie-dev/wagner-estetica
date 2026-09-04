from django.apps import AppConfig


class App2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app2'

    def ready(self):
        import os
        # Prevent running twice in debug mode (runserver)
        if os.environ.get('RUN_MAIN', None) != 'true':
            from .scheduler import start_scheduler
            start_scheduler()
