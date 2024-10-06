from django.contrib import admin
from .models import Subscribers, MailMessage

# Register your models here.

class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('email_subscriber', 'date')
    readonly_fields = ["date"]
    search_fields = ['email_subscriber', 'date', ]

class MailMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'status', 'date_de_publication_email')
    readonly_fields = ["date_de_publication_email"]
    search_fields = ['title', 'date_de_publication_email', 'message', ]


admin.site.register(Subscribers, SubscribedUsersAdmin)
admin.site.register(MailMessage, MailMessageAdmin)