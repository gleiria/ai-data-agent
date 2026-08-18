from django.contrib import admin

from agent_app.models import Customer, DailyUsage, ProductIncident, Subscription

admin.site.register(Customer)
admin.site.register(Subscription)
admin.site.register(DailyUsage)
admin.site.register(ProductIncident)
