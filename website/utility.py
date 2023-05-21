import openai
from PIL import Image, ImageFilter
from rembg import remove
import pywhatkit as pw

ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}
# openai.api_key = open("OPENAI_API_KEY.txt","r").read()
# print(openai.api_key)
UPLOAD_FOLDER = "website/uploads"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

def text_to_handwritten(text):
    filename=text[:5].replace(" ","")
    pw.text_to_handwriting(text,f"website/static/{filename}_handwritten.png",(0,0,138))
    return f"{filename}_handwritten.png"


def resizing(filename,height,width):
    image = Image.open(f"{UPLOAD_FOLDER}/resizing/{filename}")
    filename = filename.split(".")
    resize_image = image.resize((height,width))
    resize_image.save(f"website/static/{filename[0]}_resized.{filename[1]}")

    return f"{filename[0]}_resized.{filename[1]}"