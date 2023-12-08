from picamera import PiCamera
from time import sleep

camera = PiCamera()

#camera.resolution = (1920,1080)
camera.start_preview()
camera.start_recording('/home/deboradfg/Desktop/videoindoor_v2.h264')
sleep(30)
camera.stop_recording()
camera.stop_preview()                
