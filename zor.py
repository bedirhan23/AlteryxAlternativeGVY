from PIL import Image, ImageFilter
import pytesseract
import numpy as np

# Load image (this part may vary depending on your use case)
img = Image.open("zor.jpg")

# Preprocessing (example)
img = img.filter(ImageFilter.SMOOTH_MORE)

# Type check and conversion
if not isinstance(img, Image.Image):
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img)
    else:
        raise TypeError("Unsupported image type")

# Format conversion
if img.format not in ["JPEG", "PNG"]:
    img = img.convert('RGB')
    img.save('converted_image.jpg')

# OCR
text = pytesseract.image_to_string(img)
print(text)