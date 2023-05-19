import openai
from PIL import Image, ImageFilter
from rembg import remove

ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}
# openai.api_key = open("OPENAI_API_KEY.txt","r").read()
# print(openai.api_key)
UPLOAD_FOLDER = "website/static/uploads"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_image(prompt):
    response = openai.Image.create(
        prompt = prompt,
        n = 1,
        size = '1024x1024'
    )
    image = response['data'][0]['url']
    return image

def compress_image(filename):
    image = Image.open(f"{UPLOAD_FOLDER}/compression/{filename}")
    filename = filename.split(".")
    image.save(f"website/static/{filename[0]}_compressed.{filename[1]}",optimize=True,quality=5)
    return f"{filename[0]}_compressed.{filename[1]}"

def enhance_image(filename):
    image = Image.open(f"{UPLOAD_FOLDER}/enhancement/{filename}")
    filename = filename.split(".")
    enhance_image = image.filter(ImageFilter.DETAIL)
    enhance_image.save(f"website/static/{filename[0]}_enhanced.{filename[1]}")

    return f"{filename[0]}_enhanced.{filename[1]}"

def remove_bg(filename):
    image = Image.open(f"{UPLOAD_FOLDER}/backgroundRemover/{filename}")
    filename = filename.split(".")
    remove_image = remove(image)
    remove_image.save(f"website/static/{filename[0]}_remove_bg.{filename[1]}")

    return f"{filename[0]}_remove_bg.{filename[1]}"