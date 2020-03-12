import io
import picamera
from picamera import PiCamera, Color


with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.annotate_foreground = Color('yellow')
    camera.annotate_text_size = 50
    camera.annotate_text = "Pre-saved video"
    camera.start_recording('my_video.h264')
    camera.wait_recording(15)
    camera.stop_recording()