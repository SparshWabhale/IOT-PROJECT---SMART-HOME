from keras.models import load_model
from time import time
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
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
    'Sad': 'path_to_sad_song.mp3',
    'Surprise': 'path_to_surprise_song.mp3'
}

# Initialize pygame mixer for audio playback
pygame.mixer.init()

cap = cv2.VideoCapture(0)

# Define the duration for which emotions will be detected (in seconds)
duration = 10
start_time = time()
emotion_predictions = []

while time() - start_time <= duration:
    ret, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            preds = classifier.predict(roi)[0]
            label = class_labels[preds.argmax()]
            emotion_predictions.append(label)

            # Display the identified emotion label on the output box
            label_position = (x, y)
            cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

        else:
            cv2.putText(frame, 'No Face Found', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    cv2.imshow('Emotion Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Find the dominant emotion
dominant_emotion = max(set(emotion_predictions), key=emotion_predictions.count)
print(f"Dominant Emotion: {dominant_emotion}")

# Play the song based on the dominant emotion
if dominant_emotion in emotion_songs:
    song_name = emotion_songs[dominant_emotion]
    print(f"Playing: {song_name}")
    song_path = emotion_songs[dominant_emotion]
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

# Wait for the song to finish playing (optional)
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

cap.release()
cv2.destroyAllWindows()