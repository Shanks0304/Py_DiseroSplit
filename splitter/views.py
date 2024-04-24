import os
import shutil
from django.conf import settings
from django.shortcuts import render
from django.http import FileResponse, HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt  # Use this decorator to exempt CSRF for this view
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
import json
from .base_functions.file import upload_to_media, split_audio, isAlreadyExist

# Create your views here.
isKeyValied = True
isUploaded = True

def home(request):
    return render(request, 'home.html')

def verify(request):
    return render(request, 'verify.html')

def setting(request):
    return render(request, 'setting.html')

def download(request, file_name):
    context = {
        'name': file_name
    }
    return render(request, 'download.html', context = context)

@csrf_exempt  # Use this decorator with caution and only when necessary
@require_http_methods(["POST"])  # This decorator restricts this view to only handle POST requests
def split(request):
    try:  
        if request.method == 'POST':
            # Decode the request body to get the JSON data
            data = json.loads(request.body.decode('utf-8'))
            
            # Now you can access the data as a normal Python dictionary
            uploaded_file_name = data.get('file_name')
            
            isSuccess = split_audio(uploaded_file_name=uploaded_file_name)
            final_output_dir = os.path.join(settings.MEDIA_ROOT, f"downloads/{uploaded_file_name}-Stems")
            final_dir_name = os.path.basename(final_output_dir)
            return JsonResponse({'isSuccess': isSuccess, 'file_dir': final_dir_name})
        else:
            return JsonResponse({'status': 'error', 'message': 'This is not POST Request'}, status=400)

    except json.JSONDecodeError:
        # Handle JSON decoding error (e.g., if the body is not valid JSON)
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
 
@csrf_exempt  # Use this decorator with caution and only when necessary
@require_http_methods(["POST"])  # This decorator restricts this view to only handle POST requests
def upload_audio(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        print(upload_to_media(uploaded_file= uploaded_file))
        return JsonResponse({'message': 'File uploaded successfully!'})
    else:
        return JsonResponse({'error': 'No file was uploaded!'}, status=400)

@csrf_exempt  # Use this decorator with caution and only when necessary
@require_http_methods(["POST"])  # This decorator restricts this view to only handle POST requests
def output_exist(request):
    try:  
        if request.method == 'POST':
            # Decode the request body to get the JSON data
            data = json.loads(request.body.decode('utf-8'))
            
            # Now you can access the data as a normal Python dictionary
            uploaded_file_name = data.get('file_name')
            
            result = isAlreadyExist(uploaded_file_name=uploaded_file_name)
            
            return JsonResponse({'result': result})
        else:
            return JsonResponse({'status': 'error', 'message': 'This is not POST Request'}, status=400)

    except json.JSONDecodeError:
        # Handle JSON decoding error (e.g., if the body is not valid JSON)
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

@csrf_exempt  # Use this decorator with caution and only when necessary
@require_http_methods(["POST"])  # This decorator restricts this view to only handle POST requests
def download_file(request):
    try:  
        if request.method == 'POST':
            # Decode the request body to get the JSON data
            data = json.loads(request.body.decode('utf-8'))
            
            # Now you can access the data as a normal Python dictionary
            uploaded_file_name = data.get('folder_name') + '.zip'
            print(uploaded_file_name)
            download_file_path =  os.path.join(settings.BASE_DIR, uploaded_file_name)
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, f"downloads/{data.get('folder_name')}"))
            response = FileResponse(open(download_file_path, 'rb'), as_attachment=True, filename=uploaded_file_name)
            return response
            

    except json.JSONDecodeError:
        # Handle JSON decoding error (e.g., if the body is not valid JSON)
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)


# class FileDownloadView(View):
#     def post(self, request, *args, **kwargs):
#         folder_name = request.POST.get('folder_name')
#         print(folder_name)
#         download_file_path =  os.path.join(settings.BASE_DIR, folder_name)
#         if download_file_path is None:
#             return JsonResponse({"error": "No file path provided."}, status=400)

#         if not default_storage.exists(download_file_path):
#             return JsonResponse({"error": "File not found."}, status=404)

#         file = default_storage.open(download_file_path, 'rb')
#         file.close = False  # Prevent Django from automatically closing the file.
#         response = FileResponse(file)

#         return response