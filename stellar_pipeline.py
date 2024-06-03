# -*- coding: utf-8 -*-
"""stellar_pipeline.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1a8f_gtX_KXNVQX8YDhe2KLSq3mJiuVG2
"""

import numpy as np
import pandas as pd
import pickle
import os
import random
import cv2
import plotly.express as px

class Pipeline(object):
  def __init__(self, data):
    self.data = data
    self.features = ['alpha', 'delta', 'u', 'g', 'r', 'i', 'z', 'redshift']
    self.label = 'class'
    self.df = None

  def get_input(self):
    self.df = pd.DataFrame(data=self.df, columns=self.features)

  def preprocessing(self):
    with open(file='scaler.pkl', mode='rb') as scale:
      scaler = pickle.load(file=scale)

    self.df = scaler.transform(x=self.df)
    self.df = pd.DataFrame(data=self.df, columns=self.features)

  def prediction(self):
    with open(file='classifier.pkl', mode='rb') as classify:
      classifier = pickle.load(file=classify)

    prob = classifier.predict_proba(x=self.df)
    confidence = np.round(a=np.max(a=prob)*100, decimals=2)
    prediction = classifier.predict(x=self.df)[0]

    fig = self.get_image(prediction=prediction)

    if prediction=="QSO":
      prediction = "Quasi-Stellar Object"
    elif prediction=="GALAXY":
      prediction = "Galaxy"
    else:
      prediction = "Star"

    result = "Predicted class: '{}' with a confidence of {}%".format(prediction, confidence)
    return result, fig, prediction

  def get_image(self, prediction):
    image_root = os.path.join(os.getcwd(), 'path')

    if prediction == 'QSO':
      image_class_path = os.path.join(image_root, 'qsos')
    elif prediction == 'GALAXY':
      image_class_path = os.path.join(image_root, 'galaxies')
    else:
      image_class_path = os.path.join(image_root, 'stars')

    image_picked = random.choice(seq=os.listdir(path=image_class_path))
    image_picked_path = os.path.join(image_class_path, image_picked)

    image = cv2.imread(filename=image_picked_path)
    image = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB)

    image_fig = px.imshow(img=image)
    image_fig.update_layout(
        coloraxis_showscale=False,
        autosize=True, height=500,
        margin=dict(l=0, r=0, b=0, t=0)
    )
    image_fig.update_xaxes(showticklabels=False)
    image_fig.update_yaxes(showticklabels=False)
    return image_fig

  def pipeline(self):
    self.get_input()
    self.preprocessing()
    return self.predict()

