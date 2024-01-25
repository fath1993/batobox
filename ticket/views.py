import json

from django.http import JsonResponse
from django.shortcuts import render
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from custom_logs.models import custom_log
from storage.models import Storage
from ticket.models import Ticket, Message
from ticket.serializer import TicketSerializer, MessageSerializer
from utilities.http_metod import fetch_data_from_http_post, fetch_files_from_http_post_data
from utilities.utilities import create_json


class TicketView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        try:
            front_input = json.loads(request.body)
            try:
                ticket_title = front_input['ticket_title']
                if ticket_title == '':
                    return JsonResponse(
                        create_json('post', 'ساخت تیکت', 'ناموفق', f'عنوان تیکت بدرستی ارسال نشده است'))
                new_ticket = Ticket.objects.create(
                    status='ایجاد شده',
                    title=ticket_title,
                    belong_to=request.user,
                    created_by=request.user,
                    updated_by=request.user,
                )
                ticket = Ticket.objects.filter(id=new_ticket.id, belong_to=request.user)
                if ticket.count() == 0:
                    return JsonResponse(
                        create_json('post', 'ساخت تیکت', 'ناموفق', f'تیکت با ایدی {new_ticket.id} یافت نشد'))
                serializer = TicketSerializer(ticket, many=True)
                json_response_body = {
                    'method': 'post',
                    'request': 'ساخت تیکت',
                    'result': 'موفق',
                    'data': serializer.data,
                }
                return JsonResponse(json_response_body)
            except Exception as e:
                custom_log(str(e))
                return JsonResponse(
                    create_json('post', 'ساخت تیکت', 'ناموفق', f'داده ورودی کامل ارسال نشده است'))
        except Exception as e:
            print(str(e))
            return JsonResponse(create_json('post', 'ساخت تیکت', 'ناموفق', f'ورودی صحیح نیست.'))

    def put(self, request, *args, **kwargs):
        try:
            front_input = json.loads(request.body)
            try:
                try:
                    ticket_id = front_input['ticket_id']
                except:
                    return JsonResponse(
                        create_json('post', 'ویرایش تیکت', 'ناموفق', f'مقدار ticket_id ارسال نشده است'))
                try:
                    has_seen_by_user = front_input['has_seen_by_user']
                    has_seen_by_user = str(has_seen_by_user).lower()
                    if has_seen_by_user == 'false':
                        has_seen_by_user = False
                    else:
                        has_seen_by_user = True
                except:
                    return JsonResponse(
                        create_json('post', 'ویرایش تیکت', 'ناموفق', f'مقدار has_seen_by_user ارسال نشده است'))
                try:
                    ticket = Ticket.objects.get(id=ticket_id, belong_to=request.user)
                    ticket.has_seen_by_user = has_seen_by_user
                    ticket.save()
                except:
                    return JsonResponse(create_json('post', 'ویرایش تیکت', 'ناموفق', f'تیکت با ایدی {ticket_id} یافت نشد یا متعلق به کاربر فعلی نیست'))
                ticket = Ticket.objects.filter(id=ticket_id)
                if ticket.count() == 0:
                    return JsonResponse(create_json('post', 'ویرایش تیکت', 'ناموفق', f'تیکت با ایدی {ticket_id} یافت نشد'))
                serializer = TicketSerializer(ticket, many=True)
                json_response_body = {
                    'method': 'post',
                    'request': 'ویرایش تیکت',
                    'result': 'موفق',
                    'data': serializer.data,
                }
                return JsonResponse(json_response_body)
            except Exception as e:
                print(str(e))
                return JsonResponse(
                    create_json('post', 'ویرایش تیکت', 'ناموفق', f'داده ورودی کامل ارسال نشده است'))
        except Exception as e:
            print(str(e))
            return JsonResponse(create_json('post', 'ویرایش تیکت', 'ناموفق', f'ورودی صحیح نیست.'))

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class MessageNewView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        context = {}
        ticket_id = fetch_data_from_http_post(request, 'ticket_id', context)
        content = fetch_data_from_http_post(request, 'content', context)
        attachments = fetch_files_from_http_post_data(request, 'attachments', context)

        if not ticket_id:
            return JsonResponse(create_json('post', 'ساخت پیام تیکت', 'ناموفق', f'ticket_id بدرستی ارسال نشده است'))

        if not content:
            return JsonResponse(create_json('post', 'ساخت پیام تیکت', 'ناموفق', f'content بدرستی ارسال نشده است'))
        try:
            ticket = Ticket.objects.get(id=ticket_id, belong_to=request.user)
            new_message = Message.objects.create(
                ticket=ticket,
                content=content,
                created_by=request.user,
            )
            for attachment in attachments:
                new_file = Storage.objects.create(
                    alt=attachment.name,
                    file=attachment,
                    created_by=request.user,
                )
                new_message.attachments.add(new_file)
                new_message.save()
            messages = Message.objects.filter(ticket=ticket, created_by=request.user)
            serializer = MessageSerializer(messages, many=True)
            json_response_body = {
                'method': 'post',
                'request': 'ساخت پیام تیکت',
                'result': 'موفق',
                'data': serializer.data,
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            print(str(e))
            return JsonResponse(
                create_json('post', 'ساخت پیام تیکت', 'ناموفق',
                            f'تیکت با ایدی {ticket_id} یافت نشد یا دسترسی وجود ندارد'))

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class TicketListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        tickets = Ticket.objects.filter(belong_to=request.user)
        if tickets.count() == 0:
            return JsonResponse(create_json('post', 'لیست تیکت', 'ناموفق', f'لیست تیکت یافت نشد'))
        serializer = TicketSerializer(tickets, many=True)
        json_response_body = {
            'method': 'post',
            'request': 'لیست تیکت',
            'result': 'موفق',
            'data': serializer.data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class MessageListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        try:
            front_input = json.loads(request.body)
            try:
                ticket_id = front_input['ticket_id']
                messages = Message.objects.filter(ticket__id=ticket_id)
                if messages.count() == 0:
                    return JsonResponse(
                        create_json('post', 'لیست پیام های تیکت', 'ناموفق',
                                    f'تیکت با ایدی {ticket_id} یافت نشد یا دسترسی وجود ندارد'))
                serializer = MessageSerializer(messages, many=True)
                json_response_body = {
                    'method': 'post',
                    'request': 'لیست پیام های تیکت',
                    'result': 'موفق',
                    'data': serializer.data,
                }
                return JsonResponse(json_response_body)
            except Exception as e:
                print(str(e))
                return JsonResponse(
                    create_json('post', 'لیست پیام های تیکت', 'ناموفق', f'داده ورودی کامل ارسال نشده است'))
        except Exception as e:
            print(str(e))
            return JsonResponse(create_json('post', 'لیست پیام های تیکت', 'ناموفق', f'ورودی صحیح نیست.'))

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})
