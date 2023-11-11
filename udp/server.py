import cv2
import zmq
import base64

# OpenCV video capture
cap = cv2.VideoCapture(0)

# Create a ZeroMQ context and socket (PUB type)
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

while True:
    ret, frame = cap.read()
    encoded, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer)
    socket.send(jpg_as_text)
