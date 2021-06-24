"""
To be honest this program is different with the training before. My model that build from this laptop is always fail

Perhaps my laptop specification is not enough. But when I try to build from Kaggle it works. My model is 

models_kaggle.h5 ==> Download it here: https://drive.google.com/file/d/1Zqkw8I0ioDqA99YIOVmDK5T1Tmv-PpZF/view?usp=sharing
haarcascade_frontalface_default.xml ==>  Download it here: https://drive.google.com/file/d/1ZqWlVIGSZX-H1HveE2n35mkQg8ltCkhb/view?usp=sharing

Again, trust me this is not easy enough. Perhaps more than 10 hours I had been spend from begininning to the ending, but this is not end

It can be improved, I just need to walk away first

Actually, while waiting the training Process - I spend my time also watching drama 'using different device, exactly'

"""


from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import cv2

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
classifier = load_model('models_kaggle.h5')

emotion = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float')/255
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            prediction = classifier.predict(roi)[0]
            label = emotion[prediction.argmax()]
            label_position = (x, y)
            cv2.putText(frame, label, label_position,
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        else:
            cv2.putText(frame, 'No Faces Detected', (30, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Emotion Predict:', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
