# Face Recognition + Arduino Access Control

This project integrates **face recognition (Python + dlib + OpenCV)** with **Arduino** to control access via serial communication.

| Nome | RM |
|------|-----|
| Henrique Pontes Oliveira | RM98036 |
| Levy Nascimento Junior | RM98655 |
| Rafael Autieri dos Anjos | RM550885 |
| Rafael Carvalho Mattos | RM99874 |
| Vinicius Santos Yamashita de Farias | rm550885 |


---

## 🚀 Features
- Detects faces in real-time using `dlib` and `OpenCV`
- User registration (`E`) and validation (`V`)
- Saves embeddings to a local database (`db.pkl`)
- Sends a signal via **Serial (USB)** to Arduino when a registered user is recognized
- Arduino can trigger actions like:
  - Unlocking a door (servo motor)
  - Turning on an LED
  - Activating a relay

---

## 🖥️ Requirements

### Python side
- Python 3.9+
- Libraries:
  ```bash
  pip install opencv-python dlib numpy pyserial
  ```
- Model files (download and place in project folder):
  - `shape_predictor_5_face_landmarks.dat`
  - `dlib_face_recognition_resnet_model_v1.dat`

### Arduino side
- Arduino Uno / Nano / Mega
- LED or Servo connected for testing
- Serial connection (`9600 baud`)

---

## ⚙️ Usage

1. Connect your Arduino and update the correct port in `teste.py`:
   ```python
   PORT = "/dev/cu.usbserial-110"  # Mac/Linux
   # Example for Windows: PORT = "COM3"
   BAUD = 9600
   ```

2. Run the Python script:
   ```bash
   python teste.py
   ```

3. Keyboard commands:
   - **E** → Enroll user (will ask name in terminal)
   - **V** → Toggle validation ON/OFF
   - **Q** → Quit

4. When a registered user is recognized, Python sends `'O'` via serial.

---

## 🔌 Arduino Code

```cpp
#include <Servo.h>

Servo servo;
int ledPin = 13;

void setup() {
  Serial.begin(9600);
  servo.attach(9);        // Servo on pin 9
  servo.write(0);         // Locked position
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == 'O') {
      digitalWrite(ledPin, HIGH);  // Turn on LED
      servo.write(90);             // Unlock
      delay(3000);
      servo.write(0);              // Lock again
      digitalWrite(ledPin, LOW);
    }
  }
}
```

---

## 🎥 Demo
I recorded a video showing the system running:  
➡️ *[Insert link to your video]*

---

## 📂 Project Structure
```
.
├── teste.py
├── db.pkl
├── shape_predictor_5_face_landmarks.dat
├── dlib_face_recognition_resnet_model_v1.dat
└── README.md
```

---

## 🙌 Credits
Developed by **Henrique Pontes Oliveira**  
Powered by **Python, OpenCV, dlib, and Arduino**
