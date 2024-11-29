from fastapi import FastAPI, Request
from pydantic import BaseModel
import tensorflow as tf
import base64
import numpy as np
from PIL import Image, ImageOps

model = tf.keras.models.load_model("keras_model.h5")
class_names = open("labels.txt", "r").readlines()

app = FastAPI()

class ImageData(BaseModel):
    image: str


@app.put("/api")
async def predict_image(request: Request):
    input_data = await request.body()
    imgdata = base64.b64decode(input_data)
    filename = "somthing.jpg"
    
    with open(filename, "wb") as f:
        f.write(imgdata)
    
    image = Image.open(filename).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    
    result = class_name[2:]
    
    return {"class": result.strip(), "confidence": float(confidence_score)}