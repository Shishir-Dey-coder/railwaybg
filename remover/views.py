# views.py
from django.http import HttpResponse 
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from .forms import ImageUploadForm
from .models import Image
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse





def home(request):
    return render(request, "remover/home.html")
@csrf_protect
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.save()
            process_image(image)  # Process the uploaded image
            return render(request, 'remover/image_download.html', {'image': image})
    else:
        form = ImageUploadForm()
    return render(request, 'remover/image_upload.html', {'form': form})

def process_image(image):
    # Process the image using your background removal method
    # Update the 'rmbg_img' field of the Image model with the processed image
    pass



from django.shortcuts import redirect

def download_image(request, image_id):
    try:
        image = Image.objects.get(id=image_id)
    except Image.DoesNotExist:
        messages.error(request, "Image not found!")
        return redirect('home')

    if not image.rmbg_img:
        messages.error(request, "Processed image not available!")
        return redirect('home')

    response = HttpResponse(image.rmbg_img, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="processed_image.png"'
    
    messages.success(request, "Download completed!")
    
    return response
