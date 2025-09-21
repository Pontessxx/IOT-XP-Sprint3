import cv2, dlib, numpy as np, pickle, os, time
import serial

PREDICTOR = "shape_predictor_5_face_landmarks.dat"
RECOG = "dlib_face_recognition_resnet_model_v1.dat"
DB_FILE = "db.pkl"
THRESH = 0.6
PORT = "/dev/cu.usbserial-110"
BAUD = 9600

db = pickle.load(open(DB_FILE,"rb")) if os.path.exists(DB_FILE) else {}
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(PREDICTOR)
rec = dlib.face_recognition_model_v1(RECOG)

ser = serial.Serial(PORT, BAUD, timeout=0.5)
time.sleep(2)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # resolução menor
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

validando = False
ultimo = 0
cooldown = 3

print("[E]=Cadastrar  [V]=Validar ON/OFF  [Q]=Sair")

while True:
    ok, frame = cap.read()
    if not ok: break
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rects = detector(rgb, 0)   # antes era 1 → mais pesado

    for r in rects:
        shape = sp(rgb, r)
        chip = dlib.get_face_chip(rgb, shape, size=150)  # chip menor
        vec = np.array(rec.compute_face_descriptor(chip), dtype=np.float32)

        if validando and db:
            nome, dist = "Desconhecido", 999
            for n, v in db.items():
                d = np.linalg.norm(vec - v)
                if d < dist:
                    nome, dist = n, d
            if dist > THRESH:
                nome = "Desconhecido"

            color = (0,255,0) if nome != "Desconhecido" else (0,0,255)
            cv2.rectangle(frame, (r.left(), r.top()), (r.right(), r.bottom()), color, 2)
            cv2.putText(frame, f"{nome}", (r.left(), r.top()-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            if nome != "Desconhecido" and time.time()-ultimo > cooldown:
                ser.write(b'O')
                ultimo = time.time()

    cv2.imshow("Faces", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'): break
    if k == ord('v'): validando = not validando
    if k == ord('e') and len(rects) == 1:
        nome = input("Nome: ").strip()
        if nome:
            db[nome] = vec
            pickle.dump(db, open(DB_FILE,"wb"))
            print("Salvo:", nome)

cap.release()
cv2.destroyAllWindows()
ser.close()
