from flask import Flask, request, render_template, jsonify
import tensorflow as tf
import os
import numpy
import cv2
import util
app = Flask(__name__)

wsgi_app  = app.wsgi_app


@app.route('/',methods=['GET','POST'])
def main():
    
    if request.method == "POST":
        file1 = request.files["file1"].read()
        file2 = request.files["file2"].read()
        
        try:

            npimg1 = numpy.fromstring(file1, numpy.uint8)
            npimg2 = numpy.fromstring(file2, numpy.uint8)
        
            img1 = cv2.imdecode(npimg1, cv2.IMREAD_UNCHANGED)
            img2 = cv2.imdecode(npimg2, cv2.IMREAD_UNCHANGED)
        

            result = util.verify(img1,img2)
        
            return render_template("index.html",result=result)
        except:
            return render_template("index.html",message='Upload only images')
        
    return render_template("index.html")


if __name__ == '__main__':
    
    util.load_saved_artifacts()
    app.run()
