from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register
)
from .models import Subscriber
# Register your models here.

class SubscribersAdmin(ModelAdmin):
    """Define admin interface for Subscriber model"""

    model = Subscriber
    menu_label = "Subscribers"
    menu_icon = 'placeholder'
    menu_order = 500
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('email', 'last_name', 'first_name')
    search_fields = ('email', 'last_name', 'first_name')

# register our SubscriberAdmin class
modeladmin_register(SubscribersAdmin)
