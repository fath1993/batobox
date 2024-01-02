import random
import threading
import requests

'''
ثبت نام حساب
681425 
'''
'''
ورود به حساب
922176 
'''


class SendVerificationSMSThread(threading.Thread):
    def __init__(self, Mobile, TemplateId, verify_code):
        threading.Thread.__init__(self)
        self.Mobile = Mobile
        self.TemplateId = TemplateId
        self.verify_code = verify_code

    def run(self):
        url = 'https://api.sms.ir/v1/send/verify'
        headers = {
            'X-API-KEY': 'eLMoje2nCuhoG1QUmYOjAYNLSU8DQB8yD6UbYpIIaXc49d0dCivnSFemjYCYErLv'
        }
        request_body_json = {
            'Mobile': self.Mobile,
            'TemplateId': self.TemplateId,
            "parameters": [
                {
                    "name": "CODE",
                    "value": self.verify_code,
                },
            ]
        }
        print(request_body_json)
        try:
            response = requests.post(url, headers=headers, json=request_body_json)
            print(response.text)
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    SendVerificationSMSThread('09125502517', '681425', '123456').start()

