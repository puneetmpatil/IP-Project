import openai
from PIL import Image, ImageFilter
from rembg import remove
import pywhatkit as pw
import cv2
import numpy as np
import os
import argparse

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

def coloring(filename,operation):
    filename = filename.split(".")
    if operation == 'binary':
        img = cv2.imread(f"{UPLOAD_FOLDER}/coloring/{filename[0]}.{filename[1]}",2)
        ret, bw_img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        cv2.imwrite(f"website/static/{filename[0]}_colored.{filename[1]}",bw_img)

    elif operation == 'gray':
        image = Image.open(f"{UPLOAD_FOLDER}/coloring/{filename[0]}.{filename[1]}")
        color_image = image.convert("L")
        color_image.save(f"website/static/{filename[0]}_colored.{filename[1]}")

    elif operation == 'color':
        # Path to load the model
        PROTOTXT = "D:/Coding/Project/PUSHED ON GITHUB/IP-Project/website/ml_models/colorization_deploy_v2.prototxt"
        POINTS = "D:/Coding/Project/PUSHED ON GITHUB/IP-Project/website/ml_models/pts_in_hull.npy"
        MODEL = "D:/Coding/Project/PUSHED ON GITHUB/IP-Project/website/ml_models/colorization_release_v2.caffemodel"

        # Argparser
        ap = argparse.ArgumentParser()
        # ap.add_argument("-i", "--image", type=str, required=True,
	    # help="path to input black and white image")
        args = vars(ap.parse_args())

        # Load the Model
        print("Load model")
        net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
        pts = np.load(POINTS)

        # Load centers for ab channel quantization used for rebalancing.
        class8 = net.getLayerId("class8_ab")
        conv8 = net.getLayerId("conv8_313_rh")
        pts = pts.transpose().reshape(2, 313, 1, 1)
        net.getLayer(class8).blobs = [pts.astype("float32")]    
        net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

        # Load the input image
        image = cv2.imread(f"{UPLOAD_FOLDER}/coloring/{filename[0]}.{filename[1]}")
        scaled = image.astype("float32") / 255.0
        lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

        resized = cv2.resize(lab, (224, 224))
        L = cv2.split(resized)[0]
        L -= 50

        print("Colorizing the image")
        net.setInput(cv2.dnn.blobFromImage(L))
        ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
        ab = cv2.resize(ab, (image.shape[1], image.shape[0]))
        L = cv2.split(lab)[0]
        colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

        colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
        colorized = np.clip(colorized, 0, 1)

        colorized = (255 * colorized).astype("uint8")

        cv2.imwrite(f"website/static/{filename[0]}_colored.{filename[1]}",colorized)

    return f"{filename[0]}_colored.{filename[1]}"