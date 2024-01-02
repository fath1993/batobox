import os

import requests
from django.test import TestCase

from batobox.settings import BASE_URL, BASE_DIR


def test_new_message(ticket_id, content):
    url = f'{BASE_URL}ticket/api/new-message/'

    headers = {
        'Authorization': f'BatoboxToken 063072f78bdf13ac62a60c65d00f9e40f8c468b0318f31c30bd2dc02ba689eca'
    }

    data = {
        'ticket_id': f'{ticket_id}',
        'content': f'{content}',
    }

    files = {
        'attachments': open(os.path.join(BASE_DIR, 'x2.json'), 'rb'),
    }

    try:
        response = requests.post(url, headers=headers, data=data, files=files)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx status codes)

        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Unexpected status code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")