import base64
import cv2
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect('tcp://0.0.0.0:5000')

camera = cv2.VideoCapture(0)

while True:
    try:
        print('-')
        ret, frame = camera.read()
        frame = cv2.resize(frame, (640, 480))
        encoded, buf = cv2.imencode('.jpg', frame)
        image = buf.tobytes()
        
        socket.send(image)
    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        break