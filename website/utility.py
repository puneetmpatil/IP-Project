import openai
import pytesseract
from PIL import Image, ImageFilter
from rembg import remove
import cv2
import numpy as np
import os
import argparse
from os import listdir

ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}
# openai.api_key = open("OPENAI_API_KEY.txt","r").read()
# print(openai.api_key)
UPLOAD_FOLDER = "website/uploads"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convertFormat(filename,operation):
    match operation:
        case 'png':
            image = Image.open(f"{UPLOAD_FOLDER}/conversion/{filename}")
            filename = filename.split('.')[0]
            rgb_image = image.convert("RGB")
            rgb_image.save(f"website/static/{filename}.png",format='png')
            return f"{filename}.png"
        case 'jpg':
            image = Image.open(f"{UPLOAD_FOLDER}/conversion/{filename}")
            filename = filename.split('.')[0]
            rgb_image = image.convert("RGB")
            rgb_image.save(f"website/static/{filename}.jpg",format='jpeg')
            return f"{filename}.jpg"
        case 'webp':
            image = Image.open(f"{UPLOAD_FOLDER}/conversion/{filename}")
            filename = filename.split('.')[0]
            rgb_image = image.convert("RGB")
            rgb_image.save(f"website/static/{filename}.webp",format='webp')
            return f"{filename}.webp"
        case 'bmp':
            image = Image.open(f"{UPLOAD_FOLDER}/conversion/{filename}")
            filename = filename.split('.')[0]
            rgb_image = image.convert("RGB")
            rgb_image.save(f"website/static/{filename}.bmp",format='bmp')
            return f"{filename}.bmp"
        
        case 'gif':
            image = Image.open(f"{UPLOAD_FOLDER}/conversion/{filename}")
            filename = filename.split('.')[0]
            image.save(f"website/static/{filename}.gif",format='gif')
            return f"{filename}.gif"

def compress_image(filename):
    image = Image.open(f"{UPLOAD_FOLDER}/compression/{filename}")
    filename = filename.split(".")
    image.save(f"website/static/{filename[0]}_compressed.{filename[1]}",optimize=True,quality=5)
    return f"{filename[0]}_compressed.{filename[1]}"

def enhance_image(filename,style):
    image = cv2.imread(f"{UPLOAD_FOLDER}/enhancement/{filename}")
    filename = filename.split(".")

    if style == 'image_enhancement':
        # ? sigma_s => smoothening parameter, sigma_r => maintains color distinction
        output = cv2.detailEnhance(image,sigma_s=10,sigma_r = 0.15)
        cv2.imwrite(f"website/static/{filename[0]}_enhanced.{filename[1]}",output)
    elif style == 'pencil_color_sketch':
        # ? Shade factor ranges from 0 to 0.1
        imout_gray, imout = cv2.pencilSketch(image,sigma_s=60,sigma_r=0.07,shade_factor=0.05)
        cv2.imwrite(f"website/static/{filename[0]}_enhanced.{filename[1]}",imout)
    elif style == 'pencil_sketch':
        # ? Shade factor ranges from 0 to 0.1
        imout_gray, imout = cv2.pencilSketch(image,sigma_s=60,sigma_r=0.07,shade_factor=0.05)
        cv2.imwrite(f"website/static/{filename[0]}_enhanced.{filename[1]}",imout_gray)  
    elif style == 'cartoon':
        # ? Convert to gray scale
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        # ? Retrieve Edges and highlight them
        edges = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,9,8)

        # ? Color Quantization
        data = np.float32(image).reshape((-1,3))    # Defining input data for clustering

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,20,1.0)  # Define criteria

        # Applying cv2.kmeans function
        _,label,center = cv2.kmeans(data,8,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)

        # Reshape the output data to the size of input image
        result = center[label.flatten()]
        result = result.reshape(image.shape)

        # ? Smoothing the result => Median Blur
        result = cv2.medianBlur(result,3)

        # ? Combineresult and edges to get final cartoon effect
        cartoon = cv2.bitwise_and(result,result,mask=edges)
        cv2.imwrite(f"website/static/{filename[0]}_enhanced.{filename[1]}",cartoon)
    elif style == 'water_color':
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)  # Convert input image to rgb image

        result = cv2.stylization(image,sigma_s=150,sigma_r=0.25)
        cv2.imwrite(f"website/static/{filename[0]}_enhanced.{filename[1]}",result)
    # enhance_image = image.filter(ImageFilter.DETAIL)
    # enhance_image.save(f"website/static/{filename[0]}_enhanced.{filename[1]}")

    return f"{filename[0]}_enhanced.{filename[1]}"

def remove_bg(filename):
    image = Image.open(f"{UPLOAD_FOLDER}/backgroundRemover/{filename}")
    filename = filename.split(".")
    remove_image = remove(image)
    remove_image.save(f"website/static/{filename[0]}_remove_bg.{filename[1]}")

    return f"{filename[0]}_remove_bg.{filename[1]}"

def imageToPDF(filenames):
    im1=""
    count = 0
    img_list = []
    print(filenames)
    for file in filenames:
        image = Image.open(f"{UPLOAD_FOLDER}/imageToPDF/{file}")
        if count == 0:
            im1 = image.convert('RGB')
        else:
            img = image.convert('RGB')
            img_list.append(img)
        count += 1
    
    im1.save(f"website/static/finalPDF_images.pdf",save_all=True,append_images = img_list)
    return "finalPDF_images.pdf"


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

def OCR_Function(image_path):
    
    image_path = f"{UPLOAD_FOLDER}/ocr/{image_path}"
    # Open the image using PIL (Python Imaging Library)
    image = Image.open(image_path)
    
    # Convert the image to grayscale
    image = image.convert('L')
    
    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(image)
    with open("website/static/newfile.txt", 'w') as file:
        file.write(text)
    
    return "newfile.txt"
