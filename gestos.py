import mediapipe as mp
import cv2


gesture_recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(
    mp.tasks.vision.GestureRecognizerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path='modelo\gesture_recognizer.task'),
        running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
        result_callback=lambda res, _, __: print(res.gestures)
    )
)

# Captura da webcam
cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
    gesture_recognizer.recognize_async(mp_image, timestamp_ms=cv2.getTickCount())

    cv2.imshow('Gesture Recognition', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
