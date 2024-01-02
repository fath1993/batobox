from django.core.management import base

from accounts.tests import test_auth_simple, test_auth_sms_request, test_auth_auth_sms_validate, \
    test_auth_eliminate_all, test_register, test_register_confirm, test_account
from ticket.tests import test_new_message


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        while True:
            print('please choose a number:')
            print('1. test_new_message')
            try:
                choice = int(input())
                if choice == 1:
                    print('please input ticket_id:')
                    ticket_id = str(input())
                    print('please input content:')
                    content = str(input())
                    test_new_message(ticket_id, content)
                else:
                    print('not correct! try again')
            except Exception as e:
                print(str(e))
                print('not correct! try again')
