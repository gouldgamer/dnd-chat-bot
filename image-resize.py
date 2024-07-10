from PIL import Image

# Open an image file
img = Image.open('ai-ak.jpg')

# Resize the image to a specific size (e.g., 800x600)
img = img.resize((300,300))

# Save the resized image to a new file
img.save('thumbnail-ai-ak.jpg')