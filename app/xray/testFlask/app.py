from PIL import Image, ImageOps
from pydantic import BaseModel
from fastapi import FastAPI
from app.core import app
import tensorflow as tf
import numpy as np
import base64
import io

model = tf.keras.models.load_model(r"app\xray\testFlask\keras_model.h5")
class_names = open(r"app\xray\testFlask\app.py", "r").readlines()


class ImageData(BaseModel):
    image: str 

@app.put("/api/xray")
async def predict_image(image_data: ImageData):
    imgdata = base64.b64decode(image_data.image)
    image = Image.open(io.BytesIO(imgdata)).convert("RGB")
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
