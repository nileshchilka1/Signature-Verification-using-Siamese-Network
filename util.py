import numpy as np
import cv2
import base64
from tensorflow.python.keras.backend import set_session
from keras.models import load_model
import tensorflow as tf
from PIL import Image

model = None

sess = tf.Session()
graph = tf.get_default_graph()

def crop(img):
    points = cv2.findNonZero(img)
    x, y, w, h = cv2.boundingRect(points)
    return img[y: y+h, x: x+w]

def preprocess(img):
    #img = cv2.imread(img_path,1)

    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,img = cv2.threshold(img,80,255, cv2.THRESH_BINARY_INV)
    
    img = crop(img)
    ret,img = cv2.threshold(img,150,255, cv2.THRESH_BINARY_INV)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    
    open_cv_image = np.array(img) 
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    img = cv2.cvtColor(open_cv_image,cv2.COLOR_BGR2GRAY)
    
    img = np.where( img < 150,0,img)
    img = np.where(img > 200,255,img)
    
    img = cv2.resize(img,(96,96),interpolation=cv2.INTER_AREA)
    
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    return img


def verify(img1,img2):
    
    global model
    
    img1 = preprocess(img1)
    
    img2 = preprocess(img2)
    
    encoding1 = img_to_encoding(img1,model)
    
    encoding2 = img_to_encoding(img2,model)
    
    dist = round(np.linalg.norm(encoding2 - encoding1 , ord = 2),2)
    
    if dist < 0.405:
        return f'Two signatures are same with {dist}'
    else:
        return f'Two signatures are different with {dist}'



def triplet_loss(y_true, y_pred, alpha = 0.2):

    
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
    
    pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, positive)),axis=-1)
    
    neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, negative)),axis=-1)
    
    basic_loss = tf.add(tf.subtract(pos_dist, neg_dist),alpha)
    
    loss = tf.reduce_sum(tf.maximum(basic_loss,0.0))
 
    
    return loss


def load_saved_artifacts():
    print("loading saved artifacts...start")

    global model
    if model is None:
            global sess
            set_session(sess)
            model = load_model('artifacts/FRmodel.h5',custom_objects={'triplet_loss': triplet_loss})
            model._make_predict_function()
            graph = tf.get_default_graph()
    print("loading saved artifacts...done")



def img_to_encoding(img1, model):
    global graph
    global sess
    img = img1[...,::-1]
    img = np.around(np.transpose(img, (2,0,1))/255.0, decimals=12)
    x_train = np.array([img])
    
    with graph.as_default():
        set_session(sess)
        embedding = model.predict(x_train)
    return embedding


if __name__ == '__main__':  
    load_saved_artifacts()










































































