from django.db import models


class IntegerChoices(models.IntegerChoices):
    """ Adds a dict option for the IntegerChoices class"""
    @classmethod
    def dict(cls):
        return [{"id": key, "name": val} for key, val in cls.choices]
