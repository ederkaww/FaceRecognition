from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (3280, 2464)
camera.rotation = 180
sleep(1)

camera.start_preview()
try:
    for i, filename in enumerate(camera.capture_continuous('image{timestamp}.jpg')):
        print(filename)
        sleep(2)
        if i == 14:
            break
finally:
    camera.stop_preview()