from PIL import Image

# img_path = "ProcessedTraining/no_tumor/image(40).jpg"
img_path = "dory.jpg"

def is_grey_scale(img_path):
    img = Image.open(img_path).convert('RGB')
    print(type(img))
    w, h = img.size
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i,j))
            if r != g != b:
                return False
    return True

print(is_grey_scale(img_path))