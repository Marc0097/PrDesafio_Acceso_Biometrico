import cv2
import numpy as np

class CameraUtils:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

    def detectar_rostro(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Ajustamos parametros: scaleFactor 1.1, minNeighbors 3 (menos estricto)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 3, minSize=(30, 30))
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            return frame[y:y+h, x:x+w]
        return None

    def convertir_a_bytes(self, imagen):
        # Encode as JPEG
        success, encoded_img = cv2.imencode('.jpg', imagen)
        if success:
            return encoded_img.tobytes()
        return None

    def bytes_a_imagen(self, data_bytes):
        # Convert bytes to numpy array
        nparr = np.frombuffer(data_bytes, np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    def entrenar_y_predecir(self, lista_usuarios, foto_actual):
        faces = []
        labels = []
        label_to_name = {}
        
        # Necesitamos convertir la foto actual a escala de grises para predicción
        if foto_actual is None:
            return "No se detectó rostro"

        gray_actual = cv2.cvtColor(foto_actual, cv2.COLOR_BGR2GRAY)

        # Preparar datos
        valid_users_count = 0
        for usuario in lista_usuarios:
            if usuario.cara is not None:
                face_img = self.bytes_a_imagen(usuario.cara)
                if face_img is not None:
                    gray_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
                    # Resize to ensure consistency? LBPH handles different sizes but better if consistent.
                    # Just append for now
                    faces.append(gray_face)
                    labels.append(usuario.id)
                    label_to_name[usuario.id] = usuario.nombre
                    valid_users_count += 1
        
        if valid_users_count == 0:
            return "No hay usuarios registrados"

        # Entrenar
        self.recognizer.train(faces, np.array(labels))

        # Predecir
        try:
            label, confidence = self.recognizer.predict(gray_actual)
            # Confidence: 0 is perfect match. Usually < 50-80 is good match.
            # You might want to set a threshold.
            if confidence < 70: # Umbral de confianza
                return label_to_name.get(label, "Desconocido")
            else:
                return "Desconocido"
        except Exception as e:
            return f"Error: {e}"
