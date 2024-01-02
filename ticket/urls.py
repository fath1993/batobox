from django.urls import path, include

from ticket.views import MessageNewView, TicketNewView, TicketListView, MessageListView

app_name = 'ticket'

urlpatterns = [
    path('api/new-ticket/', TicketNewView.as_view(), name='new-ticket'),
    path('api/new-message/', MessageNewView.as_view(), name='new-message'),
    path('api/ticket-list/', TicketListView.as_view(), name='ticket-list'),
    path('api/message-list/', MessageListView.as_view(), name='message-list'),
]

