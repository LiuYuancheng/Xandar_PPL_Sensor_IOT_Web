import socket, cv2, numpy

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
server_socket.bind(('',5000))  
server_socket.listen(5)
capture = cv2.VideoCapture(0)
#capture = cv2.VideoCapture('my_video.h264')
# capture.set(cv2.CV_CAP_PROP_FRAME_WIDTH, 640)
# capture.set(cv2.CV_CAP_PROP_FRAME_HEIGHT, 480)

client_socket = None

while True:
    if (client_socket is None):
        client_socket, address = server_socket.accept()
#         print "Open socket whit: " , address
    _,img = capture.read()
#     print img
#     print "Tipo img: ",type(img)
#     print "Grandezza img",img.shape
#     print "Tipo di dato img: ",img.dtype
#     print "Numero di elementi: ",img.size
    data = img.tostring()
    try:
        client_socket.send(data)
    except:
        pass
    try:
        if client_socket.recv(1024)=="end":
#             print "Ho ricevuto l'end dal Client"
            client_socket.close()
            client_socket = None
        else:
            pass
#             print "Ho ricevuto il continue dal Client"
    except:
        client_socket.close()
        client_socket = None
cv2.VideoCapture(0).release()
server_socket.close()