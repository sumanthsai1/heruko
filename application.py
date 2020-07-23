import os.path
import numpy as np
import cv2
import json
from flask import Flask,request,Response,jsonify
import jsonpickle
import uuid


def diseasesDetect(img):
    #return ('Ayyappan')
    img = img
    dim = (900, 700)
    res = img
    blurred = cv2.pyrMeanShiftFiltering(img, 21, 171)
    # imgray=cv2.cvtColor(blurred,cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([11, 100, 100])
    upper_blue = np.array([25, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    ret, thresh = cv2.threshold(mask, 11, 50, cv2.THRESH_BINARY)
    # ,contours,=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE )

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print('Number of coutours:' + str(len(contours)))
    # print(contours[0])
    cv2.drawContours(res, contours, 8, (255, 0, 0), 3)
    print("Length" + str(len(contours)))
    print("Size of Contours")
    size1 = []
    for i in range(len(contours)):
        size1.append(contours[i].size)
        # print("Area",cv2.contourArea(contours[i]))
        print("Index", i, ":", contours[i].size)
    print('Maximum Size:', max(size1))
    # cv2.imshow("Image",thresh)
    value=max(size1)
    if (value > int(1500)):
        cv2.imshow("Contours Gray Image", res)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        #x={"name":"Ayyappan"}
        #return ("Ayyappan")
        return("Bacterial Leaf Blight")

application=app=Flask(__name__)
@app.route('/api/upload',methods=['POST'])
def upload():
    img=cv2.imdecode(np.fromstring(request.files['file'].read(),np.uint8),cv2.IMREAD_UNCHANGED)
    #img=cv2.imread("C:\\Users\\olive\\PycharmProjects\\openCV\DSC_0372.JPG")
    #img=request.files['image']
    imgProcess=diseasesDetect(img)
    result=jsonpickle.encode(imgProcess)
    #response=imgProcess
    print(imgProcess)
    return Response(response=imgProcess,status=imgProcess,mimetype="application/json")


app.run()