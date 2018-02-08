from flask import Flask, render_template, json, jsonify, request, Response
import io
import jsonpickle
import numpy as np
# import cv2
from PIL import Image
from Model.ModelClass import inception_retrain
#from scripts.label_image import predict_result

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 12 * 1024 * 1024 # 16 mb image
model=None

@app.route("/")
def home():
    return render_template('Interior_design.html')

@app.route("/classify", methods=['POST'])
def get_image():
    global model
    Predictions = {}

    file_object = request.files['photo']
    photo = file_object.read()
    if model is None:
        model=inception_retrain()
    pred1,pred2,pred3,pred4 = model.predict(photo)
    Predictions.update({'Bohemian':'{:.1%}'.format(pred1),'Coastal':'{:.1%}'.format(pred2),'Industrial':'{:.1%}'.format(pred3),'Scandinavian':'{:.1%}'.format(pred4)})

    return jsonify(Predictions)

# def get_filename():
#     user_data = request.get_json[]
#     n,r=int(user_data['n'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
