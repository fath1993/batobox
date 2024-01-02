from django.contrib import admin

from ticket.models import Ticket, Message


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'status',
        'title',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )

    fields = (
        'status',
        'title',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )

    def save_model(self, request, instance, form, change):
        instance = form.save(commit=False)
        if not change:
            instance.created_by = request.user
            instance.updated_by = request.user
        else:
            instance.updated_by = request.user
        instance.save()
        form.save_m2m()
        return instance


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'ticket',
        'content',
        'created_at',
        'created_by',
    )

    readonly_fields = (
        'created_at',
        'created_by',
    )

    fields = (
        'ticket',
        'content',
        'attachments',
        'created_at',
        'created_by',
    )

    def save_model(self, request, instance, form, change):
        instance = form.save(commit=False)
        if not change:
            instance.created_by = request.user
        instance.save()
        form.save_m2m()
        return instance
