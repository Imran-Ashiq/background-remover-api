import base64
from io import BytesIO
from PIL import Image


# Provide the Base64 string (replace with your actual Base64 string)

# Remove the 'data:image/jpeg;base64,' part if it exists
if base64_string.startswith("data:image"):
    base64_string = base64_string.split(",")[1]

# Ensure the Base64 string has correct padding
if len(base64_string) % 4 != 0:
    base64_string += '=' * (4 - len(base64_string) % 4)  # Ensure padding is correct

try:
    # Decode the Base64 string into bytes
    img_bytes = base64.b64decode(base64_string)

    # Print first few bytes of the image to check if it's correct
    print("First few bytes of decoded image:", img_bytes[:10])  # Print the first 10 bytes

    # Check if the decoded bytes are a valid image
    img = Image.open(BytesIO(img_bytes))

    # Save the image
    output_path = "output_image.jpg"
    img.save(output_path)
    print(f"Image has been saved as {output_path}")

except Exception as e:
    print(f"Error decoding or saving image: {e}")