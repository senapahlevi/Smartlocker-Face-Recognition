import telepot #you can use sudo install telepot in this case i am using python 3.xx so the syntax is sudo pip3 install telepot
import cv2 #this is open cv before using these make sure you install opencv for imageprocessing youcan search on google how its done.
import numpy as np
import os
import time, datetime
from telepot.loop import MessageLoop
import RPi.GPIO as GPIO
from time import sleep

servo_pins = 3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Use Board pin numbering
GPIO.setup(servo_pins, GPIO.OUT)
pwm = GPIO.PWM(servo_pins, 50)
pwm.start(0)

now = datetime.datetime.now()  # Getting date and time


def handle(msg):
    chat_id = msg['chat']['id']  # Receiving the message from telegram
    command = msg['text']  # Getting text from the message

    print(type(msg))
    print('Received:')
    print(chat_id)
    print(command)

    # Comparing the incoming message to send a reply according to it
    if command == 'tutup':
        bot.sendMessage(chat_id, str("tutup"))
        pwm.ChangeDutyCycle(2)  # neutral posisi
        sleep(1)
    elif command == '/time':
        bot.sendMessage(chat_id,
                        str("Time: ") + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second))
    elif command == '/date':
        bot.sendMessage(chat_id, str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))
    elif command == 'hidup':
        bot.sendMessage(chat_id, str("awas ada maling ges"))
        pwm.ChangeDutyCycle(2)  # neutral posisi
        sleep(1)

        # GPIO.output(red_led_pin, True)
    elif command == 'sena':
        bot.sendMessage(chat_id, str("selamat datang Sena"))
        pwm.ChangeDutyCycle(12)
        # sleep(1)

        # pintu dibuka = the door is opened
    # You can open door using chat telegram,
    elif command == 'buka':
        bot.sendMessage(chat_id, str("Pintu dibuka dengan telegram"))
        pwm.ChangeDutyCycle(12)
        sleep(1)
    return


bot = telepot.Bot('1035745322:AAGr786rgp5pzSwLgAH08GBbvB84Q_Lwoko')
print(bot.getMe())
# Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
bot.message_loop(handle)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

# iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Sena', 'faisal', 'rizqy', 'garoxZ', 'Wkwkwk']

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video widht
cam.set(4, 480)  # set video height

# Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

while True:

    ret, img = cam.read()
    img = cv2.flip(img, 1)  # Flip vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 50):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))

            msg = {}
            msg["chat"] = {}
            msg['chat']['id'] = '1048188423'
            msg["text"] = "sena"
            handle(msg)

        # elif(confidence ):
        # GPIO.output(5, GPIO.LOW)

        else:

            id = "unknown"
            msg = {}
            msg["chat"] = {}
            msg['chat']['id'] = '1048188423'
            msg["text"] = "hidup"
            handle(msg)

            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    cv2.imshow('camera', img)

    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
