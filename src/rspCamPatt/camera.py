from picamera import PiCamera, Color
from time import sleep
camera = PiCamera()
camera.resolution = (640, 480)
# camera.start_preview()
camera.start_recording('my_video.h264')
camera.annotate_foreground = Color('yellow')
camera.annotate_text_size = 50
camera.annotate_text = "Pre-saved video!"
sleep(15)
# camera.stop_preview()