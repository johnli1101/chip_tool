#image adjusting when given 4 points of the smaller image size and the corresponding 4 points on larger image
@app.route('/imageAdjust', methods=['POST'])
def api_image_adjust():
    request_data = request.get_json();
    print(request_data);
    
    small = cv2.imread(request_data["instruction"]["image"])
    #small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
    small2 = Image.open(request_data["instruction"]["image"])

    big = cv2.imread(request_data["original"]["image"])
    #big = cv2.cvtColor(big, cv2.COLOR_BGR2RGB)
    big2 = Image.open(request_data["original"]["image"])

    #big = (width, height)=(3393, 2622)
    #small = (width, height)=(653, 741)

    wl, hl = big2.size
    ws, hs = small2.size

    bH, bW = big.shape[:2]
    sH, sW = small.shape[:2]

    big_size = big2.size

    m1 = float(request_data["instruction"]["points"][0][0]);
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
    a = max(x1, x2, x3, x4)+ wl
    b = max(y1, y2, y3, y4)+ hl
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
    transformed = cv2.warpPerspective(empty, M, (bH1, bW1))

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
        out1.save(os.path.join(app.config['UPLOAD_FOLDER']  + "instructions_adj/", new_filename), "PNG")
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
        transformed = cv2.warpPerspective(empty, M, (bH, bW))

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
        out2.save(os.path.join(app.config['UPLOAD_FOLDER']  + "instructions_adj", new_filename), "PNG")

        width, height = out2.size
        print("Size of output image is: ", width, height)

    return app.config["UPLOAD_FOLDER"] + "instructions_adj/" + str(new_filename)