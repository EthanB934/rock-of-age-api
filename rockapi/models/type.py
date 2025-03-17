# Base class needed for creating tables in database
from django.db import models

class Type(models.Model):
    """A class representing a database table"""
    # Property of Type object, representative of table column
    label = models.CharField(max_length=155)