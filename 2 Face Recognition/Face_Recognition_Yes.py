import cv2
import face_recognition
import os
import pyttsx3

#cv2: OpenCV library for computer vision tasks.
#face_recognition: A face recognition library built on top of dlib.
#os: Operating system module for interacting with the operating system.
#pyttsx3: A Python library for text-to-speech conversion.

engine = pyttsx3.init()
cv2.namedWindow("Laptop Webcam")

path = 'Images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = face_recognition.load_image_file(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

#It appends the images to the images list and extracts the class names (names of people)
# without file extensions using os.path.splitext().

def findEncodings(images):
    encodeList = []
    for img in images:
        encode = face_recognition.face_encodings(img)
        if encode:
            encodeList.append(encode[0])
    return encodeList

encodeListKnown = findEncodings(images)
print('Encoding Complete')

#This function, findEncodings, takes a list of images as input and returns a list of
# face encodings using face_recognition.face_encodings().
# It checks if any face is detected in an image before appending the encoding to the list.

cap = cv2.VideoCapture(0)
#This line initializes the webcam capture using OpenCV.
speak = ""

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)

    if not facesCurFrame:
        name = "No Face Detected"
        speak = name
        print(name)
        cv2.imshow('Webcam', img)
        engine.say(speak)
        engine.runAndWait()
        cv2.waitKey(2)
        continue  # Skip the rest of the loop if no faces are detected

    # The code enters a loop where it reads frames from the webcam, resizes them, and converts them to RGB format.
    # The resizing is done to improve performance.

    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    faceDis = face_recognition.face_distance(encodeListKnown, encodeCurFrame[0])
    matchIndex = faceDis.argmin()

    if faceDis[matchIndex] < 0.6:  # You can adjust this threshold
        name = classNames[matchIndex].upper()
        speak = f"Access Granted. Welcome {name}"
        print(speak)
        y1, x2, y2, x1 = facesCurFrame[0]
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imshow('Webcam', img)
        engine.say(speak)
        engine.runAndWait()
        cv2.waitKey(1)
    else:
        name = "Access Denied"
        speak = name
        print(name)
        cv2.imshow('Webcam', img)
        engine.say(speak)
        engine.runAndWait()
        cv2.waitKey(2)
