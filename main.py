import mediapipe as mp
import cv2
import subprocess

ultimo_gesto = ""
contador_open_palm = 0
contador_closed_fist = 0
LIMITE_CONTAGEM = 100

# Flags para evitar múltiplas ativações
ativado_open_palm = False
ativado_closed_fist = False

# URLs de ativação
url_open_palm = "https://www.virtualsmarthome.xyz/url_routine_trigger/activate.php?trigger=0eb359cb-53ee-4f81-bc24-73e50b1814ed&token=de91721a-e71c-4148-afbf-4ec2258118b6&response=html"
url_closed_fist = "https://www.virtualsmarthome.xyz/url_routine_trigger/activate.php?trigger=9661b7b7-ca64-4943-8135-694646fa29b9&token=af2cab24-131d-4c09-b8a2-f27fafbd0162&response=html"

def callback(res, _, __):
    global ultimo_gesto
    global contador_open_palm, contador_closed_fist
    global ativado_open_palm, ativado_closed_fist

    if res.gestures:
        gesto_atual = res.gestures[0][0].category_name
        ultimo_gesto = gesto_atual
        print(gesto_atual)

        # Verifica e atualiza contadores
        if gesto_atual == "Open_Palm":
            contador_open_palm += 1
            contador_closed_fist = 0
        elif gesto_atual == "Closed_Fist":
            contador_closed_fist += 1
            contador_open_palm = 0
        else:
            contador_open_palm = 0
            contador_closed_fist = 0
            ativado_open_palm = False
            ativado_closed_fist = False

        # Verifica ativação de Open_Palm
        if contador_open_palm >= LIMITE_CONTAGEM and not ativado_open_palm:
            subprocess.Popen(["python", "ativador.py", url_open_palm])
            print("Chamando ativador.py para Open_Palm...")
            ativado_open_palm = True

        # Verifica ativação de Closed_Fist
        if contador_closed_fist >= LIMITE_CONTAGEM and not ativado_closed_fist:
            subprocess.Popen(["python", "ativador.py", url_closed_fist])
            print("Chamando ativador.py para Closed_Fist...")
            ativado_closed_fist = True

gesture_recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(
    mp.tasks.vision.GestureRecognizerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path='modelo\\gesture_recognizer.task'),
        running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
        result_callback=callback
    )
)

cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
    gesture_recognizer.recognize_async(mp_image, timestamp_ms=cv2.getTickCount())

    cv2.putText(image, f'Gesto: {ultimo_gesto}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Gesture Recognition', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
