from django.apps import AppConfig


class OneOhOneCoreConfig(AppConfig):
    name = "one_oh_one_core"
    verbose_name = "101 Core"

    def ready(self):
        import one_oh_one_core.signals