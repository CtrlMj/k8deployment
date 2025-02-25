import grpc
from PIL import Image
import numpy as np
from io import BytesIO
from urllib import request as urlrequeast
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc
# import tensorflow as tf
from flask import Flask, request, jsonify
from proto import np_to_protobuf
import os

classes = [
    "dress",
    "hat",
    "longsleeve",
    "outwear",
    "pants",
    "shirts",
    "shoes",
    "shorts",
    "skirts",
    "t-shirt"
]

host = os.getenv("TF_SERVING_HOST", "localhost:8500")
channel = grpc.insecure_channel(host)
stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

app = Flask("gateway")

def read_image(url):
    with urlrequeast.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    img = img.resize((299, 299), Image.NEAREST)
    return img

def preprocess_input(x):
    x = x / 127.5
    x -= 1.
    return x

def create_proto_request(x):
    pb_request = predict_pb2.PredictRequest()
    pb_request.model_spec.name = "clothes-classifier"
    pb_request.model_spec.signature_name = "serving_default"
    pb_request.inputs['input_2'].CopyFrom(np_to_protobuf(x))
    return pb_request

def prepare_response(pbr):
    preds = pbr.outputs['dense_1'].float_val
    return dict(zip(classes, preds))

def predict(url):
    img = read_image(url)
    X = np.array([img])
    X = preprocess_input(X)
    pb_request = create_proto_request(X)
    pb_response = stub.Predict(pb_request, timeout=20.0)
    response = prepare_response(pb_response)
    return response

@app.route("/predict", methods=["POST"])
def predict_endpoint():
    data = request.get_json()
    url = data['url']
    result = predict(url)
    return jsonify(result)

if __name__=='__main__':
    # url = 'http://bit.ly/mlbookcamp-pants'
    # response = predict(url)
    # print(response)
    app.run(debug=True, host='0.0.0.0', port=9696)

    