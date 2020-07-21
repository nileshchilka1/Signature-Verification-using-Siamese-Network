from flask import Flask, request, render_template, jsonify
import import_ipynb
import tensorflow as tf
import util
image_data1 = None
image_data2 = None
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def main():
    return render_template('app.html')

@app.route('/signature_verification1', methods=['POST'])
def signature_verification1():
    global image_data1
    image_data1 = request.form['image_data1']
    return 'hi'

@app.route('/signature_verification2', methods=[ 'POST'])
def signature_verification2():
    global image_data2
    image_data2 = request.form['image_data2']
    return 'hi'

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    global image_data1
    global image_data2
    result = util.verify(image_data1,image_data2)
    return render_template('app.html', result=result)

if __name__ == '__main__':
    
    util.load_saved_artifacts()
    app.run()
