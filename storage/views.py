import os
import time

import jdatetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from gallery.models import FileGallery
from PIL import Image
import io
from django.core.files.base import ContentFile
from django.core.paginator import Paginator

from utilities.http_metod import fetch_data_from_http_post, fetch_single_file_from_http_file, fetch_data_from_http_get
from utilities.slug_generator import name_to_url
from yekjamodir.settings import BASE_URL


class FilesList(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'page_title': 'فایل های من',
                        'navigation_icon_menu_id': 'storage',
                        'navigation_menu_body_id': 'navigationStorage',
                        'navigation_menu_body_main_item_id': 'file-manager',
                        'navigation_menu_body_sub_item_id': 'files-list',
                        'breadcrumb_1': 'خانه',
                        'breadcrumb_2': 'ذخیره سازی',
                        'breadcrumb_3': 'مدیریت فایل',
                        }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            searched_word = fetch_data_from_http_get(request, 'searched_word', self.context)
            if searched_word:
                searched_files_list = []
                files = FileGallery.objects.filter(created_by=request.user)
                files_by_alt = files.filter(alt__icontains=searched_word)
                for file_by_alt in files_by_alt:
                    searched_files_list.append(file_by_alt)
                for file_by_path in files:
                    if str(file_by_path.file.name).find(searched_word) != -1:
                        searched_files_list.append(file_by_path)
                files = list(set(searched_files_list))
            else:
                files = FileGallery.objects.filter(created_by=request.user)
            paginator = Paginator(files, 50)  # Show 25 contacts per page.

            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            self.context['page_obj'] = page_obj
            return render(request, 'file-manager/files-list.html', self.context)
        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, '404.html')
        else:
            return redirect('accounts:login')


def file_allowed_to_upload(http_request_file):
    http_request_file_size = int(http_request_file.seek(0, 2) / (1024 * 1024))  # in mega byte
    if http_request_file_size > 50:
        print('maximum allowed file size is 50 Mb')
        return False
    else:
        return True


def user_quote_limit_exceed(file_size_list, user):
    new_files_size = 0
    for file_size in file_size_list:
        new_files_size += file_size
    user_file_size = user_all_file_size_in_mb(user)
    sum_of_size = user_file_size + (new_files_size / (1024 * 1024))
    user_maximum_quota = user_maximum_quote_size_in_mb(user)
    if sum_of_size > user_maximum_quota:
        return [True, sum_of_size, user_maximum_quota]
    else:
        return [False]


def file_processor(http_request_file, user):
    http_request_file_is_image = False
    allowed_image_types = ['image/jpeg', 'image/png']
    if http_request_file.content_type in allowed_image_types:
        http_request_file_is_image = True
    base_name, original_extension = os.path.splitext(http_request_file.name)
    http_request_file.name = f'{name_to_url(base_name)}{original_extension}'
    if http_request_file_is_image:
        new_file = image_processor(http_request_file=http_request_file, alt=http_request_file.name, user=user)
    else:
        new_file = FileGallery.objects.create(alt=http_request_file.name, file=http_request_file, created_by=user)
    return new_file


def image_processor(http_request_file, alt, user, target_size_in_kb):
    if int(target_size_in_kb) > http_request_file.size:
        target_size_in_kb = http_request_file.size
    # Open the image file
    img = Image.open(http_request_file)

    # Define the target file size (100KB in bytes)
    target_size = int(target_size_in_kb) * 1024

    # Convert image to RGB for JPEG compression (if not already)
    img = img.convert("RGB")

    # Compress the image until the file size is under the target size
    while True:
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='JPEG', optimize=True, quality=70)
        '''The processed image is saved to the img_byte_array, which is an in-memory bytes IO stream (io.BytesIO()). 
        It doesn't save to a file on your filesystem; instead, it saves the processed image data directly into the 
        img_byte_array object in memory.'''

        current_size = img_byte_array.tell()
        try:
            if current_size <= target_size:
                img_byte_array.seek(0)
                content_file = ContentFile(img_byte_array.getvalue())
                processed_image = FileGallery.objects.create(
                    alt=alt,
                    created_by=user
                )
                processed_image.file.save(http_request_file.name, content_file)
                return processed_image
        except Exception as e:
            print(str(e))

        # Resize the image to reduce the size
        new_width = int(img.width * 0.9)
        new_height = int(img.height * 0.9)
        img = img.resize((new_width, new_height))


def upload_permission_view(request):
    context = {}
    message = 'allowed'
    if request.method == 'POST':
        print(request.POST)
        file_size = fetch_data_from_http_post(request, 'fileSize', context)
        file_size_list = [int(file_size)]

        for file_size in file_size_list:
            if int(file_size) / (1024 * 1024) > 50:
                message = 'حد اکثر حجم هر کدام از فایل های انتخابی 50 مگابایت می باشد'
        u_q_l_e = user_quote_limit_exceed(file_size_list, request.user)
        if u_q_l_e[0]:
            message = f'فضای ذخیره شما کافی نیست. {u_q_l_e[1]} / {u_q_l_e[2]}'
    else:
        message = 'not allowed'
    return JsonResponse({'message': message})


def upload_files_view(request):
    context = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            file_alt = fetch_data_from_http_post(request, 'file_alt', context)
            file = fetch_single_file_from_http_file(request, 'file', context)
            image_compress_size = fetch_data_from_http_post(request, 'image_compress_size', context)

            if image_compress_size:
                try:
                    image_compress_size = int(image_compress_size)
                    if image_compress_size > file.size:
                        return JsonResponse({'message': 'سایز مورد نظر بزرگتر از سایز اصلی تصویر است'})
                    elif image_compress_size < 20:
                        return JsonResponse({'message': 'حد اکثر انتخاب قابل فشرده سازی 20 کیلوبایت است'})
                    else:
                        new_image = image_processor(file, file_alt, request.user, image_compress_size)
                        return JsonResponse({'message': 'succeed',
                                             'file_id': f'{new_image.id}',
                                             # 'file_url': f'http://127.0.0.1:8000{new_image.file.url}'})
                                             'file_url': f'{BASE_URL}{new_image.file.url}'})
                except:
                    return JsonResponse({'message': 'سایز مورد نظر امکان پذیر نیست'})

            new_file = FileGallery(
                alt=file_alt,
                file=file,
                created_by=request.user,
            )
            new_file.save()
            return JsonResponse({'message': 'succeed',
                                 'file_id': f'{new_file.id}',
                                 # 'file_url': f'http://127.0.0.1:8000{new_file.file.url}'})
                                 'file_url': f'{BASE_URL}{new_file.file.url}'})
        else:
            return JsonResponse({'message': 'failed'})
    else:
        return JsonResponse({'message': 'failed'})


def ajax_file_remove(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            file_id = fetch_data_from_http_post(request, 'file_id', {})
            if file_id is None:
                return JsonResponse({'message': 'failed. file_id'})
            try:
                file = FileGallery.objects.get(id=file_id, created_by=request.user)
                try:
                    os.remove(file.file.path)
                except:
                    pass
                file.delete()
            except Exception as e:
                print(str(e))
                return JsonResponse({'message': 'failed. insufficient privilege'})
        return JsonResponse({'message': 'succeed'})
    else:
        return JsonResponse({'message': 'failed. unknown user'})


def ajax_user_storage_analyzer(request):
    if request.user.is_authenticated:
        try:
            user_files = FileGallery.objects.filter(created_by=request.user)
            all_files_size = 0  # in byte

            image_files_size = 0
            image_file_list = []
            video_files_size = 0
            video_file_list = []
            document_files_size = 0
            document_file_list = []
            system_files_size = 0
            system_file_list = []
            other_files_size = 0
            other_file_list = []
            for file in user_files:
                try:
                    all_files_size += file.file.size
                    if file_ext(file.file.path) == '.png' or file_ext(file.file.path) == '.jpg' or file_ext(
                            file.file.path) == '.jpeg' or file_ext(file.file.path) == '.gif' or file_ext(
                        file.file.path) == '.bmp' or file_ext(file.file.path) == '.tiff' or file_ext(
                        file.file.path) == '.webp' or file_ext(file.file.path) == '.psd':
                        image_file_list.append(file.file)
                    elif file_ext(file.file.path) == '.mp4' or file_ext(file.file.path) == '.avi' or file_ext(
                            file.file.path) == '.mov' or file_ext(file.file.path) == '.mkv' or file_ext(
                        file.file.path) == '.wmv' or file_ext(file.file.path) == '.flv' or file_ext(
                        file.file.path) == '.webm' or file_ext(file.file.path) == '.m4v' or file_ext(
                        file.file.path) == '.mpg' or file_ext(file.file.path) == '.mpeg' or file_ext(
                        file.file.path) == '.3gp':
                        video_file_list.append(file.file)
                    elif file_ext(file.file.path) == '.pdf' or file_ext(file.file.path) == '.txt' or file_ext(
                            file.file.path) == '.doc' or file_ext(file.file.path) == '.docx' or file_ext(
                        file.file.path) == '.xls' or file_ext(file.file.path) == '.xlsx' or file_ext(
                        file.file.path) == '.ppt' or file_ext(file.file.path) == '.pptx' or file_ext(
                        file.file.path) == '.odt' or file_ext(file.file.path) == '.ods' or file_ext(
                        file.file.path) == '.odp':
                        document_file_list.append(file.file)
                    elif file_ext(file.file.path) == '.exe' or file_ext(file.file.path) == '.zip' or file_ext(
                            file.file.path) == '.rar' or file_ext(file.file.path) == '.dll' or file_ext(
                        file.file.path) == '.sys' or file_ext(file.file.path) == '.app' or file_ext(
                        file.file.path) == '.bat':
                        system_file_list.append(file.file)
                    else:
                        other_file_list.append(file.file)
                except:
                    pass

            for image_file in image_file_list:
                image_files_size += image_file.size
            for video_file in video_file_list:
                video_files_size += video_file.size
            for document_file in document_file_list:
                document_files_size += document_file.size
            for system_file in system_file_list:
                system_files_size += system_file.size
            for other_file in other_file_list:
                other_files_size += other_file.size

            all_files_size_with_ext = number_with_ext(all_files_size / (1024 * 1024))
            image_files_size_with_ext = number_with_ext(image_files_size / (1024 * 1024))
            video_files_size_with_ext = number_with_ext(video_files_size / (1024 * 1024))
            document_files_size_with_ext = number_with_ext(document_files_size / (1024 * 1024))
            system_files_size_with_ext = number_with_ext(system_files_size / (1024 * 1024))
            other_files_size_with_ext = number_with_ext(other_files_size / (1024 * 1024))

            today = jdatetime.datetime.now()
            user_maximum_quota = request.user.profile_user.default_maximum_storage_quota
            has_vip_plan = False
            if request.user.profile_user.vip_plan_expiry_date:
                if request.user.profile_user.vip_plan_expiry_date > today:
                    has_vip_plan = True
                    user_maximum_quota += request.user.profile_user.vip_plan.maximum_storage_quota
            if request.user.profile_user.extra_storage_expiry_date:
                if request.user.profile_user.extra_storage_expiry_date > today:
                    has_vip_plan = True
                    user_maximum_quota += request.user.profile_user.extra_storage.storage
            if has_vip_plan:
                user_maximum_quota -= request.user.profile_user.default_maximum_storage_quota

            json_response_body = {
                'result': {
                    'image_files_number': len(image_file_list),
                    'video_files_number': len(video_file_list),
                    'document_files_number': len(document_file_list),
                    'system_files_number': len(system_file_list),
                    'other_files_number': len(other_file_list),
                    'all_files_size': all_files_size_with_ext,
                    'image_files_size': image_files_size_with_ext,
                    'video_files_size': video_files_size_with_ext,
                    'document_files_size': document_files_size_with_ext,
                    'system_files_size': system_files_size_with_ext,
                    'other_files_size': other_files_size_with_ext,
                    'image_files_percent': int(((image_files_size / (1024 * 1024)) / user_maximum_quota) * 100),
                    'video_files_percent': int(((video_files_size / (1024 * 1024)) / user_maximum_quota) * 100),
                    'document_files_percent': int(((document_files_size / (1024 * 1024)) / user_maximum_quota) * 100),
                    'system_files_percent': int(((system_files_size / (1024 * 1024)) / user_maximum_quota) * 100),
                    'other_files_percent': int(((other_files_size / (1024 * 1024)) / user_maximum_quota) * 100)
                }
            }
            return JsonResponse(json_response_body)
        except Exception as e:
            return JsonResponse({'message': 'failed',
                                 'err': str(e)})
    else:
        return JsonResponse({'message': 'failed'})


def user_all_file_size_in_mb(user):
    files_size = 0
    user_files = FileGallery.objects.filter(created_by=user)
    for file in user_files:
        try:
            files_size += file.file.size
        except:
            pass
    sum_of_size = int(files_size / (1024 * 1024))
    return sum_of_size


def user_maximum_quote_size_in_mb(user):
    today = jdatetime.datetime.now()
    user_maximum_quota = user.profile_user.default_maximum_storage_quota
    has_vip_plan = False
    if user.profile_user.vip_plan_expiry_date:
        if user.profile_user.vip_plan_expiry_date > today:
            has_vip_plan = True
            user_maximum_quota += user.profile_user.vip_plan.maximum_storage_quota
    if user.profile_user.extra_storage_expiry_date:
        if user.profile_user.extra_storage_expiry_date > today:
            has_vip_plan = True
            user_maximum_quota += user.profile_user.extra_storage.storage
    if has_vip_plan:
        user_maximum_quota -= user.profile_user.default_maximum_storage_quota
    return user_maximum_quota


def file_ext(file_path):
    base_name, original_extension = os.path.splitext(file_path)
    return original_extension


def number_with_ext(number_in_mb):
    value = number_in_mb * 1024 * 1024
    if 0 <= value <= 1024:
        return f'{int(value)} B'
    elif 1024 < value <= 1024 * 1024:
        return f'{int(value / 1024)} Kb'
    elif 1024 * 1024 < value < 1024 * 1024 * 1024:
        return f'{int(value / (1024 * 1024))} Mb'
    elif 1024 * 1024 * 1024 < value < 1024 * 1024 * 1024 * 1024:
        return f'{int(value / (1024 * 1024 * 1024))} Gb'
    else:
        return f'{value} unknown'