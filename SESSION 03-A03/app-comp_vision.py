from flask import Flask
import ghhops_server as hs
import rhino3dm
import numpy as np
import os
import sys

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

app = Flask(__name__)
hops = hs.Hops(app)


@hops.component(
    "/runml",
    name="runml",
    description="Run Machine Learning prediction",
    icon="examples/pointat.png",
    #inputs=[
    #    hs.HopsCurve("Curve", "C", "Curve to evaluate"),
    #    hs.HopsNumber("t", "t", "Parameter on Curve to evaluate"),
    #],
    #outputs=[
    #    hs.HopsPoint("P", "P", "Point on curve at t")
    #]
)




#FIND DEPENDENCIES
path_model = "pattern_model.h5"
print("Dependencies OK")

#LOAD MODEL
new_model = tf.keras.models.load_model(path_model)
#new_model.summary()
print("Model OK")

#LOAD QUERY
query_flat = np.loadtxt("query.txt") #load
query = np.reshape(query_flat,(128,128,3))
query = query.astype(np.float32)
query_norm = np.multiply(query, 2)
query_norm = np.subtract(query_norm , 1)  #normalize -1 to 1, it is already 0 to 1
query_t = tf.convert_to_tensor(query_norm)
query_t = tf.expand_dims(query_t, 0)

#MAKE PREDICTION
IMG_WIDTH = 128
IMG_HEIGHT = 128
CHANNELS = 3

def plot(tensor):
    array = np.asarray(tensor)
    array = array.astype('float64')
    array = array.reshape(IMG_HEIGHT, IMG_WIDTH,CHANNELS)
    return array

def generate_images(model, test_input):
    prediction = model(test_input, training=True)

    # remap to [0,1]
    test_input = test_input * 0.5 + 0.5
    prediction = prediction * 0.5 + 0.5

    display_list = [plot(test_input), plot(prediction)]
    title = ['Input Image', 'Predicted Image']

    for i in range(2):
        plt.subplot(1, 2, i + 1)
        plt.title(title[i])
        # getting the pixel values between [0, 1] to plot it.
        plt.imshow(display_list[i])
        plt.axis('off')
    plt.draw()
    plt.savefig("D:\German Profile\Desktop\PREDICTION MODEL\log.png")

    return prediction

pred = generate_images(new_model,query_t)
print("Prediction OK")

#SAVE TO FOLDER
pred = np.reshape(pred,(128,128,3))
np.savetxt("prediction.txt", pred.flatten())
print("text Saved")

img = Image.fromarray(np.uint8(pred * 255), 'RGB')
img.save("pred_image.png")
print("imagesaved")


if __name__ == "__main__":
    app.run()