import tkinter as tk
from tkinter import messagebox, simpledialog
import cv2
import sys
import os

# Ensure we can import from src if running purely as script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.usuario_dao import UsuarioDAO
from src.utils.camera_utils import CameraUtils

class BioPassApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BioPass DAO - Acceso Biométrico")
        self.root.geometry("400x300")

        self.dao = UsuarioDAO()
        self.camera = CameraUtils()

        # UI Elements
        self.label = tk.Label(root, text="BioPass System", font=("Arial", 16))
        self.label.pack(pady=20)

        self.btn_registrar = tk.Button(root, text="Registrar Usuario", command=self.registrar_usuario, width=20, height=2)
        self.btn_registrar.pack(pady=10)

        self.btn_login = tk.Button(root, text="Entrar (Login)", command=self.login_usuario, width=20, height=2)
        self.btn_login.pack(pady=10)

    def capturar_foto(self):
        """Muestra video en vivo y captura foto al pulsar ESPACIO."""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "No se detectó la cámara")
            return None
        
        messagebox.showinfo("Instrucción", "Se abrirá la cámara. Pulsa ESPACIO para tomar la foto.")
        
        frame_capturado = None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Dibujar instrucciones en el video
            debug_frame = frame.copy()
            cv2.putText(debug_frame, "Pulsa ESPACIO para capturar", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow("Cámara BioPass", debug_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 32: # Espacio
                frame_capturado = frame
                break
            elif key == 27: # Esc
                break

        cap.release()
        cv2.destroyAllWindows()
        
        if frame_capturado is None:
            # Si cerro sin capturar
            return None
            
        return frame_capturado

    def registrar_usuario(self):
        nombre = simpledialog.askstring("Registro", "Introduce tu nombre:")
        if not nombre:
            return

        # messagebox.showinfo("Instrucción", "Mira a la cámara y pulsa OK para capturar tu foto.")
        frame = self.capturar_foto()
        
        if frame is not None:
            # Procesar
            face_img = self.camera.detectar_rostro(frame)
            if face_img is None:
                messagebox.showerror("Error", "No se detectó ningún rostro. Inténtalo de nuevo.")
                return

            foto_bytes = self.camera.convertir_a_bytes(frame)
            cara_bytes = self.camera.convertir_a_bytes(face_img)

            if foto_bytes and cara_bytes:
                self.dao.registrar_usuario(nombre, foto_bytes, cara_bytes)
                messagebox.showinfo("Éxito", f"Usuario '{nombre}' registrado correctamente.")
            else:
                messagebox.showerror("Error", "Error al procesar la imagen.")

    def login_usuario(self):
        # messagebox.showinfo("Instrucción", "Mira a la cámara y pulsa OK para entrar.")
        frame = self.capturar_foto()
        
        if frame is not None:
            face_img = self.camera.detectar_rostro(frame)
            if face_img is None:
                messagebox.showerror("Error", "No se detectó ningún rostro.")
                return

            # Obtener usuarios y entrenar
            usuarios = self.dao.obtener_todos()
            resultado = self.camera.entrenar_y_predecir(usuarios, face_img)
            
            if resultado == "Desconocido":
                messagebox.showwarning("Acceso Denegado", "No se reconoce el usuario.")
            elif resultado.startswith("Error") or resultado.startswith("No"):
                 messagebox.showerror("Error", resultado)
            else:
                messagebox.showinfo("Acceso Permitido", f"Bienvenido, {resultado}!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BioPassApp(root)
    root.mainloop()
