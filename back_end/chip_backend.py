import flask
from flask import request, jsonify, send_file, send_from_directory, url_for
from flask_cors import CORS, cross_origin
import urllib.request
import ntpath
from pathlib import Path
import json
import io
from io import BytesIO
import base64
from base64 import encodebytes
import requests
import os
from os import getcwd # only import "getcwd" from os
from werkzeug.utils import secure_filename
import sys
import cv2
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import matplotlib.pyplot as plt

cors = CORS()

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors.init_app(app=app, supports_credentials=True)
app.config['UPLOAD_FOLDER'] = getcwd() + "/../front_end/public/chip_images/"
app.config['UPLOAD_FOLDER2'] = getcwd() + "/../front_end/src/assets/transparent/"
app.config['UPLOAD_FOLDER3'] = getcwd() + "/static/";
 
# MYSQL Setup
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'school_map'

# mysql = MySQL(app)

#uploads image marker image to the assets directory
@app.route('/uploadImageInstructions', methods=['POST'])
def api_upload_image_instructions():
    print(request.files)
    
    file = request.files['file']
    folder = "instructions"

    filename = secure_filename(file.filename)
    filepath = app.config['UPLOAD_FOLDER'] + str(folder) + "/" + str(filename)

    #check if file exists if not then upload the image
    my_file = Path(filepath)
    print(my_file)
    if not my_file.is_file():
        file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + folder, filename))

    return filepath

#uploads image marker image to the assets directory
@app.route('/uploadImageOriginals', methods=['POST'])
def api_upload_image_originals():
    print(request.files)
    
    file = request.files['file']
    folder = "originals"

    filename = secure_filename(file.filename)
    filepath = app.config['UPLOAD_FOLDER'] + str(folder) + "/" + str(filename)

    #check if file exists if not then upload the image
    my_file = Path(filepath)
    print(my_file)
    if not my_file.is_file():
        file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + folder, filename))

    return filepath

#uploads image marker image to the assets directory
@app.route('/uploadImage', methods=['POST'])
def api_upload_image():
    print(request.files)
    
    file = request.files['file']
    folder = request.files['folder']
    print(folder);

    filename = secure_filename(file.filename)
    filepath = app.config['UPLOAD_FOLDER'] + str(folder) + "/" + str(filename)

    #check if file exists if not then upload the image
    my_file = Path(filepath)
    print(my_file)
    if not my_file.is_file():
        file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + folder, filename))

    return filepath

#uploads image marker image to the assets directory
@app.route('/uploadImageFinal', methods=['POST'])
def api_upload_image_final():
    print(request.files)
    
    file = request.files['file']
    folder = 'final'
    print(folder);

    filename = secure_filename(file.filename)
    # filepath = app.config['UPLOAD_FOLDER'] + str(folder) + "/" + str(filename)
    filepath = app.config['UPLOAD_FOLDER3'] + "final/" + str(filename);

    #check if file exists if not then upload the image
    # my_file = Path(filepath)
    # print(my_file)
    # if not my_file.is_file():
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + folder, filename))
    file.save(os.path.join(app.config['UPLOAD_FOLDER3'] + "final/", filename))

    return filepath

#creates final image with the drawn lines pasted over the exported chip image
@app.route('/createFinalExport', methods=['POST'])
def api_create_final_export():
    request_data = request.get_json()
    print(request_data);

    user_drawing=Image.open(app.config['UPLOAD_FOLDER3'] + "/final/file.png")
    chip_background=Image.open(app.config['UPLOAD_FOLDER3'] + "/export/exported_image.png")
    filename=request_data['filename'] + ".png"

    user_drawing.convert('RGBA')
    chip_background.paste(user_drawing, (0, 0), user_drawing)
    chip_background.save(app.config['UPLOAD_FOLDER3'] + "/final_export/" + filename, quality=95)



    # create file-object in memory
    file_object = io.BytesIO()

    chip_background.save(file_object, 'PNG')

    file_object.seek(0)

    return send_file(file_object, mimetype='image/PNG')
    #return send_from_directory(directory=app.config['UPLOAD_FOLDER'] + "/final_export/", path=filename)

#executes command line given, in this case this is specifically made to open gimp (but can call any command line)
@app.route('/launchGimp', methods=['POST'])
def api_launch_gimp():
    request_data = request.get_json()
    print(request_data);

    os.system(str(request_data["command"]))

    return "Successful";

#for creating the final image based off of the template selected
@app.route('/createExport', methods=['POST'])
def api_create_export():
    request_data = request.get_json()
    print(request_data)

    #template chosen
    template = request_data["template"]

    # Opening the front ic chip image
    frontImg = Image.open(request_data["front_url"])
    
    # Opening the back ic chip image
    backImg = Image.open(request_data["back_url"])

    #get the sizes of front and back images (both front and back sides should have the same sizes)
    imgWidth, imgHeight = frontImg.size

    #depending on the template selection, set blank width and height accordingly
    #the chips should have 100 px offset on each side
    blankWidth = 0
    blankHeight = 0
    backImgOffsetX = 0
    backImgOffsetY = 0

    if template == 'A':
        blankWidth = imgWidth * 2 + 400
        blankHeight = imgHeight + 200
        backImgOffsetX = blankWidth-(imgWidth+100)
        backImgOffsetY = 100
        
    # elif template == 'B':

    elif template == 'C':
        blankWidth = imgWidth + 200
        blankHeight = imgHeight * 2 + 400
        backImgOffsetX = 100
        backImgOffsetY = blankHeight-(imgHeight+100)

    # elif template == 'D':

    else:
        return "error invalid template"

    #create blank image based off of the image sizes
    print(str(imgWidth) + " " + str(imgHeight))
    print(str(blankWidth) + " " + str(blankHeight) + " " + str(backImgOffsetX) + " " + str(backImgOffsetY))
    imgBlank = Image.new("RGB", (blankWidth, blankHeight), (255, 255, 255))

    #paste both images onto here with offsets of 100 from both sides
    imgBlank.paste(frontImg, (100, 100), mask=frontImg)
    imgBlank.paste(backImg, (backImgOffsetX, backImgOffsetY), mask=backImg)

    #created file name and save it in the path
    filename = "exported_image.png"
    #filepath = app.config['UPLOAD_FOLDER'] + "exported/" + str(filename)
    filepath = app.config['UPLOAD_FOLDER3'] + "export/" + str(filename);
    print(filepath)
    #imgBlank.save(os.path.join(app.config['UPLOAD_FOLDER']  + "exported/", filename))
    imgBlank.save(os.path.join(app.config['UPLOAD_FOLDER3']  + "export/", filename))

    payload = {}

    payload["filepath"] = filepath
    payload["filesize"] = [blankWidth, blankHeight]

    print(payload);

    return payload

@app.route('/croppedImageUpload', methods=['POST'])
def api_cropped_image_upload():
    request_data = request.get_json();
    print(request_data);
    if not request_data['same']:
        starter = request_data["image"].find(',')
        image_data = request_data["image"][starter+1:]
        image_data = bytes(image_data, encoding="ascii")
        im = Image.open(BytesIO(base64.b64decode(image_data)))

        filename_split, file_extension = os.path.splitext(request_data["filename"])
        print(filename_split);
        new_filename = str(filename_split) + "_cropped" + str(file_extension);

    else: 
        im = Image.open(request_data["image"])
        new_filename = request_data["filename"]

    im.save("static/image_cropped/" + str(new_filename), "PNG")
    new_filepath = app.config['UPLOAD_FOLDER3'] + "image_cropped/" + str(new_filename);

    return new_filepath;

@app.route('/paintImageUpload', methods=['POST'])
def api_paint_image_upload():
    request_data = request.get_json();
    print(request_data);

    starter = request_data["image"].find(',')
    image_data = request_data["image"][starter+1:]
    image_data = bytes(image_data, encoding="ascii")
    im = Image.open(BytesIO(base64.b64decode(image_data)))

    filename_split, file_extension = os.path.splitext(request_data["filename"])
    print(filename_split);
    new_filename = str(filename_split) + "_paint" + str(file_extension);

    im.save("static/paint/" + str(new_filename), "PNG")
    new_filepath = app.config['UPLOAD_FOLDER3'] + "paint/" + str(new_filename);

    return new_filepath;

#image adjusting when given 4 points of the smaller image size and the corresponding 4 points on larger image
@app.route('/imageAdjust', methods=['POST'])
def api_image_adjust():
    request_data = request.get_json();
    print(request_data);
    
    small = cv2.imread(request_data["instruction"]["image"])
    #small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
    small2 = Image.open(request_data["instruction"]["image"])
    print(small2.size)

    big = cv2.imread(request_data["original"]["image"])
    #big = cv2.cvtColor(big, cv2.COLOR_BGR2RGB)
    big2 = Image.open(request_data["original"]["image"])
    print(big2.size)

    #big = (width, height)=(3393, 2622)
    #small = (width, height)=(653, 741)

    wl, hl = big2.size
    ws, hs = small2.size

    bH, bW = big.shape[:2]
    sH, sW = small.shape[:2]

    big_size = big2.size

    m1 = float(request_data["instruction"]["points"][0][0])
    n1 = float(request_data["instruction"]["points"][0][1])
    m2 = float(request_data["instruction"]["points"][1][0])
    n2 = float(request_data["instruction"]["points"][1][1])
    m3 = float(request_data["instruction"]["points"][2][0])
    n3 = float(request_data["instruction"]["points"][2][1])
    m4 = float(request_data["instruction"]["points"][3][0])
    n4 = float(request_data["instruction"]["points"][3][1])

    x1 = float(request_data["original"]["points"][0][0])
    y1 = float(request_data["original"]["points"][0][1])
    x2 = float(request_data["original"]["points"][1][0])
    y2 = float(request_data["original"]["points"][1][1])
    x3 = float(request_data["original"]["points"][2][0])
    y3 = float(request_data["original"]["points"][2][1])
    x4 = float(request_data["original"]["points"][3][0])
    y4 = float(request_data["original"]["points"][3][1])

    inp = np.float32([[m1, n1], [m2, n2], [m3, n3], [m4, n4]])
    out = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

    filename = ntpath.basename(request_data["instruction"]["image"]);
    print(filename);
    filename_split, file_extension = os.path.splitext(filename)
    print(filename_split);
    new_filename = str(filename_split) + "_adj" + str(file_extension);

    if (x1<0 or x1>wl-ws or x2>wl or x3>wl or x4<0 or x4>wl-ws or y1<0 or y1>hl-hs or y2>hl-hs or y3>hl or y4>hl):
        #new_size is optional size, it is how much black border we want to padd:
        a = max(x1, x2, x3, x4)+ wl + ws - min(m1, m2, m3, m4)
        b = max(y1, y2, y3, y4)+ hl + hs - min(n1, n2, n3, n4)

        new_size = (int(a), int(b))
        new_im = Image.new("RGB", new_size)   ## luckily, this is already black!
        new_im.paste(big2, (int((new_size[0]-big_size[0])/2), int((new_size[1]-big_size[1])/2)))
        
        new_im.save('new.jpg')
        new = cv2.imread('new.jpg')
        #new = cv2.cvtColor(new, cv2.COLOR_BGR2RGB)
        new[:] = (0, 0, 0)
        bH1, bW1 = new.shape[:2]
        sH, sW = small.shape[:2]

        empty = 0 * np.ones((bH1, bW1, 3), dtype=np.uint8)
        empty[:sH, :sW] = small

        # Cordinates: TopLeft, TopRight, BottomRight, BottomLeft
        inp = np.float32([[m1, n1], [m2, n2], [m3, n3], [m4, n4]])
        out = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

        
        M, status = cv2.findHomography(inp, out)
        transformed = cv2.warpPerspective(empty, M, (bW1, bH1))
    
        new[np.where(transformed != 0)] = transformed[np.where(transformed != 0)]
        
        cv2.imwrite('out-final.png', new)
        out1 = Image.open("out-final.png")

        out1 = out1.convert("RGBA")
        datas = out1.getdata()

        newData = []
        for item in datas:
            if item[0] == 0 and item[1] == 0 and item[2] == 0:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        out1.putdata(newData)
        #out1.save(os.path.join(app.config['UPLOAD_FOLDER']  + "instructions_adj/", new_filename), "PNG")
        out1.save("static/" + str(new_filename), "PNG");
        #out1.save("out-final2.png", "PNG")
        
        width, height = out1.size
        print("Size of output image is: ", width, height)
        

    else:
        empty = 0 * np.ones((bH, bW, 3), dtype=np.uint8)
        empty[:sH, :sW] = small
        big[:] = (0, 0, 0)

        # Cordinates: TopLeft, TopRight, BottomRight, BottomLeft
        inp = np.float32([[m1, n1], [m2, n2], [m3, n3], [m4, n4]])
        out = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])


        M, status = cv2.findHomography(inp, out)
        transformed = cv2.warpPerspective(empty, M, (bW, bH))

        big[np.where(transformed != 0)] = transformed[np.where(transformed != 0)]
            
        cv2.imwrite('out-normal.png', big)
        out2 = Image.open("out-normal.png")

        out2 = out2.convert("RGBA")
        datas = out2.getdata()

        newData = []
        for item in datas:
            if item[0] == 0 and item[1] == 0 and item[2] == 0:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        out2.putdata(newData)

        #out2.save("out-normal2.png", "PNG")
        #out2.save(os.path.join(app.config['UPLOAD_FOLDER']  + "instructions_adj", new_filename), "PNG")
        out2.save("static/" + str(new_filename), "PNG");

        width, height = out2.size
        print("Size of output image is: ", width, height)

    #return app.config["UPLOAD_FOLDER"] + "instructions_adj/" + str(new_filename)
    #finalPath = app.config["UPLOAD_FOLDER"] + "instructions_adj/" + str(new_filename)
    # return url_for('static', filename=new_filename)
    new_filepath = app.config['UPLOAD_FOLDER3'] + str(new_filename);

    return new_filepath;

#uploads image marker image to the assets directory
@app.route('/overlay', methods=['POST'])
def api_overlay():
    request_data = request.get_json();
    print(request_data);

    # filename = secure_filename(file.filename)
    # filepath = app.config['UPLOAD_FOLDER'] + str(folder) + "/" + str(filename)

    # Opening the primary image (used in background)
    img1 = Image.open(request_data["original_url"])
    
    # Opening the secondary image (overlay image)
    img2 = Image.open(request_data["instruction_url"])
    

    TRANSPARENCY = request_data["opacity"]       # percentage 

    if img2.mode!='RGBA':
        alpha = Image.new('L', img2.size, 255)
        img2.putalpha(alpha)

    paste_mask = img2.split()[3].point(lambda i: i * TRANSPARENCY / 100.)
    img1.paste(img2, (0,0), mask=paste_mask)

    # Pasting img2 image on top of img1 
    # starting at coordinates (0, 0)
    #img1.paste(img2, (0,0), mask = img2)
    
    # img1.blend(bg, fg, .7).save("out.png")
    # Displaying the image
    # img1.show()

    filename = ntpath.basename(request_data["original_url"]);
    print(filename);
    filename_split, file_extension = os.path.splitext(filename)
    print(filename_split);
    new_filename = str(filename_split) + "_transparent" + str(file_extension);

    folder = "transparencies"
    new_filepath = app.config['UPLOAD_FOLDER'] + str(folder) + "/" + str(new_filename)
    print(new_filepath)

    my_file = Path(new_filepath)
    # print(my_file)
    # if my_file.is_file():
    #     os.remove(my_file)
    #     time.sleep(2)

    #check if file exists if not then upload the image
    img1.save(os.path.join(app.config['UPLOAD_FOLDER']  + str(folder), new_filename))
    # img1.save(os.path.join(app.config['UPLOAD_FOLDER2'], new_filename))
    # print(app.config['UPLOAD_FOLDER2'] + "/" + str(new_filename))
    # return app.config['UPLOAD_FOLDER2'] + str(new_filename)

    # if my_file.is_file():
    #     new_filename = str(filename_split) + "_transparent2" + str(file_extension);
    #     img1.save(os.path.join(app.config['UPLOAD_FOLDER2'], new_filename))
    #     return app.config['UPLOAD_FOLDER2'] + "/" + str(new_filename)
    # else: 
    #     #check if file exists if not then upload the image
    #     img1.save(os.path.join(app.config['UPLOAD_FOLDER2'], new_filename))
    #     return new_filepath

    # return filepath
    return new_filepath

#for error handling of unknown status
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run(host='0.0.0.0')