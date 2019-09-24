import cv2
import os
import argparse
from encodefaces import encodefaces 

class registerface:
    def registerfacemethod(self,username):        
        # use name as folder name
        name = username
        folder = "./dataset/{}".format(name)

        # Create a new folder for the new name
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # Start the camera
        cam = cv2.VideoCapture(0)
        # Set video width
        cam.set(3, 640)
        # Set video height
        cam.set(4, 480)
        # Get the pre-built classifier that had been trained on 3 million faces
        face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        img_counter = 0
        while img_counter <= 10:
            key = input("Press q to quit or ENTER to continue: ")
            if key == "q":
                break
            
            ret, frame = cam.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            if(len(faces) == 0):
                print("No face detected, please try again")
                continue
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                img_name = "{}/{:04}.jpg".format(folder, img_counter)
                cv2.imwrite(img_name, frame[y : y + h, x : x + w])
                print("{} written!".format(img_name))
                img_counter += 1
        
        cam.release()

        ef = encodefaces()
        ef.encodef()