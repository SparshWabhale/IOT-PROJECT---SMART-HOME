import cv2
import os
import shutil
import pyttsx3

#r = sr.Recognizer()
cam = cv2.VideoCapture(0)
#url = 'http://192.168.29.92'
cv2.namedWindow("Pythong Webcam")

img_counter = 0

def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

while(1):
    ret, frame = cam.read()
    if not ret:
        print("Failed to Grab Frame")
        break

    cv2.imshow("test",frame)
    k= cv2.waitKey(1)

    if k%256 == 27:
        print("Escape hit, closing app")
        break

    elif k%256 == 32:
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name,frame)
        print("Screenshot taken")
        img_counter+=1
        if(img_counter == 1):
            break

MyText = input("Enter name :")
new_file_name = "{}.png".format(MyText)
os.rename(img_name, new_file_name.format(".png"))
source_dir = 'D:/COLLEGE/FALL SEMESTER/IOT/DEMO/'
destination_dir = 'D:/COLLEGE/FALL SEMESTER/IOT/DEMO/Images/'
shutil.move(source_dir + new_file_name, destination_dir + new_file_name)
cam.release()
#cam.destroyAllWindows()