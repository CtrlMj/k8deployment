FROM tensorflow/serving:2.8.0
COPY clothes-classifier /models/clothes-classifier/1
ENV MODEL_NAME="clothes-classifier"

