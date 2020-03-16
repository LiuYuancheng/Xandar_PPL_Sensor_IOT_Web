import socket, cv2, numpy
import imageio

client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(('172.27.140.222',5000))

while True:
    data=client_socket.recv(4096000)
    #print data
    a1D = numpy.frombuffer(data.decode('utf-8'),dtype=numpy.uint8)
    try:
        img = numpy.reshape(a1D,(480,640,3))
    except Exception as detail:
        img= numpy.zeros((480,640,3))
#         print "Error:",detail
#     print img
#     print "Tipo img: ",type(img)
#     print "Grandezza img",img.shape
#     print "Tipo di dato img: ",img.dtype
#     print "Numero di elementi: ",img.size
    cv2.imshow("It works?",img)
    #imageio.imwrite('filename.jpg', img)
    key=cv2.waitKey(33)
    if key==ord('a'):
        client_socket.send(b"end")
        break
    else:
        client_socket.send(b"continue")
    data = None
cv2.destroyAllWindows()