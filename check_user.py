from tensorflow.keras.models import load_model
import tensorflow as tf
import cv2

from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep
import numpy as np


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

red_pin = 16
green_pin = 21
blue_pin = 20
button_pin = 26

CATEGORIES = ["Anna", "Dominika", "Unknown"]

GPIO.setup(red_pin, GPIO.OUT) 
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT) 
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

camera = PiCamera()
camera.rotation = 180
camera.resolution = (3280, 2464) 

def prepare_photo(filepath):
    IMG_SIZE = 200
    img_array = cv2.imread(filepath) 
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(1, IMG_SIZE, IMG_SIZE, 3)

def turn_off():
    GPIO.output(red_pin,GPIO.LOW)
    GPIO.output(green_pin,GPIO.LOW)
    GPIO.output(blue_pin,GPIO.LOW)

def white():
    GPIO.output(red_pin,GPIO.HIGH)
    GPIO.output(green_pin,GPIO.HIGH)
    GPIO.output(blue_pin,GPIO.HIGH)

def light_blue():
    GPIO.output(red_pin, GPIO.LOW) 
    GPIO.output(green_pin, GPIO.HIGH)
    GPIO.output(blue_pin, GPIO.HIGH) 
     
def yellow():
    GPIO.output(red_pin, GPIO.HIGH)
    GPIO.output(green_pin, GPIO.HIGH)
    GPIO.output(blue_pin, GPIO.LOW) 
    
def green():
    GPIO.output(red_pin, GPIO.LOW)
    GPIO.output(green_pin, GPIO.HIGH)
    GPIO.output(blue_pin, GPIO.LOW) 
     
def red():
    GPIO.output(red_pin, GPIO.HIGH)
    GPIO.output(green_pin, GPIO.LOW)
    GPIO.output(blue_pin, GPIO.LOW)


white() 

GPIO.wait_for_edge(button_pin, GPIO.FALLING)

light_blue()

sleep(3)
camera.capture('user_photo.jpg')
sleep(2)

yellow()

model = tf.keras.models.load_model("anna_dominika_unknown.h5")
prediction = model.predict([prepare_photo('user_photo.jpg')])     
               
index = np.argmax(prediction) 

user = CATEGORIES[index] 
print('User: ', user)
                  
if index == 2:  
    print('Access denied')
    red()
else:
    print('Hello ', user)
    green()
    
sleep(5)
turn_off()
