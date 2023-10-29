# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 12:25:24 2023

@author: Gebruiker
"""
import numpy as np
import os
from flask import Flask, render_template, request
from tensorflow import keras
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

model = keras.models.load_model("C:\\Users\\Gebruiker\\Documents\\Flask\\models\\predict_age_model.h5")

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = "/Users/Gebruiker/Documents/Flask/static/images/"

@app.route('/', methods = ['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def predict_age():
    
    # Specify the folder path where you want to delete files
    folder_path = "static/images/"
    
    # List all files in the folder
    file_list = os.listdir(folder_path)
    
    # Iterate through the list of files and delete each one
    for filename in file_list:
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            
            
    imagefile = request.files['imagefile']
    image_path =  imagefile.filename
    filename = (image_path)
    image_path= 'static/images/'+ imagefile.filename
    imagefile.save(image_path)
    #basedir = os.path.abspath(os.path.dirname(__file__))
    #imagefile.save(os.path.join(basedir, app.config["IMAGE_UPLOADS"]))
    
    img = image.load_img(image_path, target_size=(64, 64))  # Zorg ervoor dat je de juiste breedte en hoogte gebruikt
    
    # Converteer de afbeelding naar een numpy-array
    img_array = image.img_to_array(img)
    
    # Voorverwerking van de afbeelding, zoals normalisatie
    img_array = img_array / 255.0  # Normaliseer de pixelwaarden
    
    # Voorspelling maken met het getrainde model
    prediction = model.predict(np.expand_dims(img_array, axis=0))  # Voeg een extra dimensie toe voor de batch
    age = round(prediction[0][0])
    old = 0
    if(age > 42):
        old = 1
    
    return render_template('index.html',  prediction=age, filename=filename, old = old)

if __name__ == "__main__":
    app.run(port=3030, debug=True)