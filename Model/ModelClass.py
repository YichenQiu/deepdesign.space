import pickle as pk
import numpy as np
import os
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from keras.models import load_model
import cv2

import numpy as np


class inception_retrain(object):
    def __init__(self):
        self.img=None
        self.model=None
        self.InV3model=None

    def _load_image(self,img):
        '''Takes an image
            Returns its proper form to feed into model's predcition '''
        #image = cv2.imread('test/{}'.format(img))
        nparr = np.fromstring(img, np.uint8)
        image = cv2.imdecode(nparr, -1)[:,:,:3]
        image = cv2.resize(image, (299, 299))
        image = np.expand_dims(image/255, axis=0)
        image = np.vstack([image])
        return image

    def _feature_extraction_inception(self,img):
        image=self._load_image(img)
        self.img=image
        features=self.InV3model.predict(image)
        return features

    def _load_model(self):
        if self.model is None:
            self.model=load_model('inV3_last_layer.h5')
        if self.InV3model is None:
            self.InV3model=load_model("inception.h5")

    def predict(self,img):
        '''Takes an imagebbb
           Return the predicted probabilities for each class'''
        self._load_model()
        image=self._feature_extraction_inception(img)
        self.img=image
        pred=self.model.predict(image)
        pred=np.round(pred,3).reshape(4,)
        return pred[0],pred[1],pred[2],pred[3]
