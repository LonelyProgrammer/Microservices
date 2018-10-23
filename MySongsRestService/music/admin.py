# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Songs

# Register your models here.
#we can use the admin section to add songs, so that we can manually test this endpoint
admin.site.register(Songs)
