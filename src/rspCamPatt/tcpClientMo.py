import socket, cv2, numpy
import imageio
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(('127.0.0.31',5000))

motion_list = [ None, None ] 
static_back = None
while True:
    data=client_socket.recv(4096000)
    #print data
    a1D = numpy.fromstring(data,dtype=numpy.uint8)
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
    motion = 0
    imageio.imwrite('filename.jpg', img)
    frame = cv2.imread('filename.jpg')
    # Converting color image to gray_scale image 
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) 
  
    # Converting gray scale image to GaussianBlur  
    # so that change can be find easily 
    gray = cv2.GaussianBlur(gray, (21, 21), 0) 
  
    # In first iteration we assign the value  
    # of static_back to our first frame 
    if static_back is None: 
        static_back = gray 
        continue
  
    # Difference between static background  
    # and current frame(which is GaussianBlur) 
    diff_frame = cv2.absdiff(static_back, gray) 
  
    # If change in between static background and 
    # current frame is greater than 30 it will show white color(255) 
    thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1] 
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2) 
  
    # Finding contour of moving object 
    (_, cnts, _) = cv2.findContours(thresh_frame.copy(),  
                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

    for contour in cnts: 
        if cv2.contourArea(contour) < 10000: 
            continue
        motion = 1
  
        (x, y, w, h) = cv2.boundingRect(contour) 
        # making green rectangle arround the moving object 
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)  
    motion_list.append(motion) 
  
    motion_list = motion_list[-2:]


    cv2.imshow("It works?",frame)
    key=cv2.waitKey(33)
    if key==27:
        client_socket.send(b"end")
        break
    else:
        client_socket.send(b"continue")
    data = None
cv2.destroyAllWindows()