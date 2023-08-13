from django.contrib import admin
from .models import Room, Message

# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    list_display=('body','sent_by','created_at','created_by')

class RoomAdmin(admin.ModelAdmin):
    list_display=('uuid', 'client','agent','url', 'display_messages','status', 'created_at' ) #list_display can't have many-many field:messages, define a method

    def display_messages(self, obj):
        return ', '.join([message.text for message in obj.messages.all()])
    display_messages.short_description = 'Messages'


admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)


