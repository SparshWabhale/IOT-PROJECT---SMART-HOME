from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
import cv2
import numpy as np
import pygame

face_classifier = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
classifier = load_model('./Emotion_Detection.h5')

class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Define the mapping between emotions and songs
emotion_songs = {
    'Angry': 'angry.mp3',
    'Happy': 'Specialz.mp3',
    'Neutral': 'path_to_neutral_song.mp3',
    'Sad': 'sad.mp3',
    'Surprise': 'path_to_surprise_song.mp3'
}

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Load the image
image_path = 'Happy.jpg'  # Replace with the path to your image file
frame = cv2.imread(image_path)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = face_classifier.detectMultiScale(gray, 1.3, 5)

emotion_detected = False

for (x, y, w, h) in faces:
    roi_gray = gray[y:y + h, x:x + w]
    roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

    if np.sum([roi_gray]) != 0:
        roi = roi_gray.astype('float') / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        preds = classifier.predict(roi)[0]
        label = class_labels[preds.argmax()]

        # Display the identified emotion label on the image
        label_position = (x, y)
        cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

        # Play the song based on the detected emotion
        if label in emotion_songs:
            song_path = emotion_songs[label]
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            emotion_detected = True

# Display the image with emotion label
cv2.imshow('Emotion Detector', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Wait for the song to finish playing (optional)
while pygame.mixer.music.get_busy() and emotion_detected:
    pygame.time.Clock().tick(10)
