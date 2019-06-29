from django.apps import AppConfig


class WebboardConfig(AppConfig):
    name = 'webboard'

    verbose_name = ""

    def ready(self):
        print('readyyyyyyyyyyyy')
        import webboard.signals
