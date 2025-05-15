from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job.accounts'

    def ready(self):
        # This ensures signals.py gets loaded when the app starts
        import job.accounts.signals

