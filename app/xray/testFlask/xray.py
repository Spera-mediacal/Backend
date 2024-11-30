from fastapi import FastAPI, UploadFile, File
import tensorflow as tf
import base64
from app.core import app
import numpy as np
from PIL import Image, ImageOps
from io import BytesIO

class CustomDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        if 'groups' in kwargs:
            del kwargs['groups']
        super().__init__(*args, **kwargs)

model = tf.keras.models.load_model(r"app\xray\testFlask\keras_model.h5", custom_objects={'DepthwiseConv2D': CustomDepthwiseConv2D})
class_names = open(r"app\xray\testFlask\labels.txt", "r").readlines()



@app.post("/api/xray", tags=['xray'])
async def index(file: UploadFile = File(...)):
    # Read the uploaded file
    imgdata = await file.read()

    # Convert the image data to a PIL Image
    image = Image.open(BytesIO(imgdata)).convert("RGB")
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    
    # Resize the image to the model's expected input size
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    
    # Normalize the image
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    
    # Make the prediction
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = float(prediction[0][index])

    result = class_name[2:].strip()
    return {"prediction": result, "confidence_score": confidence_score}
