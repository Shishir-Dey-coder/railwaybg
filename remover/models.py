from django.db import models
import numpy as np
from PIL import Image as PILImage
from rembg import remove
from io import BytesIO
import os
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

class Image(models.Model):
    # Primary key field with auto-increment
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='images/')
    rmbg_img = models.ImageField(upload_to='images_rmbg/', blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the model first

        try:
            # Open the original image using the file path
            pil_img = PILImage.open(self.img.path)
            
            # Ensure uploaded file is an image
            if pil_img.format not in ['JPEG', 'PNG', 'JPG']:
                raise ValidationError("Only JPEG, PNG, and JPG formats are supported.")

            # Convert the PIL image to bytes
            img_bytes = BytesIO()
            pil_img.save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()

            # Use rembg to remove the background
            rmbg_bytes = remove(img_bytes)

            buffer = BytesIO(rmbg_bytes)
            # Convert the bytes back to a PIL Image
            output_img = PILImage.open(buffer)

            # Secure file naming
            filename = os.path.basename(self.img.name)
            name, _ = os.path.splitext(filename)
            safe_name = ''.join(c if c.isalnum() else '_' for c in name)
            
            self.rmbg_img.save(f"bgrm_{safe_name}.png", ContentFile(rmbg_bytes), save=False)

        except Exception as e:
            # Handle any exceptions that occur during processing or saving
            print(f"An error occurred: {e}")

            # Rollback if an exception occurs during save
            self.rmbg_img.delete(save=False)
            raise e

        super().save(*args, **kwargs)  # Save the model again after processing

