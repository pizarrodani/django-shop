from django.contrib import admin

# Register your models here.

from core.models import (
    Category,
    Band,
    Product,
    Client,
    Order
)

admin.site.register(Category)
admin.site.register(Band)
admin.site.register(Product)
admin.site.register(Client)
admin.site.register(Order)
