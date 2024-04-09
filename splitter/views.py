from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # Use this decorator to exempt CSRF for this view
from django.views.decorators.http import require_http_methods
import json
from .base_functions.file import upload_to_media, split_audio

# Create your views here.
isKeyValied = True
isUploaded = True

def home(request):
    context = {
        'isKeyVerified': isKeyValied,
        'isUploaded': isUploaded,
        'audioName': 'Source Sans.wav',
    }
    return render(request, 'home.html', context=context)

def verify(request):
    return render(request, 'verify.html')

def setting(request):
    return render(request, 'setting.html')

@csrf_exempt  # Use this decorator with caution and only when necessary
@require_http_methods(["POST"])  # This decorator restricts this view to only handle POST requests
def split(request):
    try:  
        if request.method == 'POST':
            # Decode the request body to get the JSON data
            data = json.loads(request.body.decode('utf-8'))
            
            # Now you can access the data as a normal Python dictionary
            uploaded_file_name = data.get('file_name')
            
            split_audio(uploaded_file_name=uploaded_file_name)
            
            return JsonResponse({'isFinished': True})
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
