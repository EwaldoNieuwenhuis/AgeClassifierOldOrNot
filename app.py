# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 12:25:24 2023

@author: Gebruiker
"""
import os
from flask import Flask, render_template, request
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

model = keras.models.load_model("C:\\Users\\Gebruiker\\Documents\\Flask\\models\\predict_age_model.h5")

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = "/Users/Gebruiker/Documents/Flask/static/images/"

# Toegestane bestandsextensies
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict_age():
    # Folder voor het verwijderen van bestanden
    folder_path = "static/images/"
    
    # Lijst van bestanden in de map
    file_list = os.listdir(folder_path)
    
    # Loop door de lijst van bestanden en verwijder elk bestand
    for filename in file_list:
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    imagefile = request.files['imagefile']
    
    # Controleer of het bestand is toegestaan
    if imagefile and allowed_file(imagefile.filename):
        image_path = os.path.join(app.config['IMAGE_UPLOADS'], secure_filename(imagefile.filename))
        imagefile.save(image_path)
        
        img = image.load_img(image_path, target_size=(64, 64))  # Zorg ervoor dat je de juiste breedte en hoogte gebruikt

        # Converteer de afbeelding naar een numpy-array
        img_array = image.img_to_array(img)

        # Voorverwerking van de afbeelding, zoals normalisatie
        img_array = img_array / 255.0  # Normaliseer de pixelwaarden

        # Voorspelling maken met het getrainde model
        prediction = model.predict(np.expand_dims(img_array, axis=0))  # Voeg een extra dimensie toe voor de batch
        age = round(prediction[0][0])
        old = 0
        if age > 42:
            old = 1

        return render_template('index.html', prediction=age, filename=secure_filename(imagefile.filename), old=old)
    else:
        return "Ongeldig bestandsformaat. Alleen JPEG en PNG zijn toegestaan."

if __name__ == "__main__":
    app.run(port=3030, debug=True)
