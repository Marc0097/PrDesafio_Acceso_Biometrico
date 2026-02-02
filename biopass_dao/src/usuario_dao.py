from src.conexion_db import DBConnection
import psycopg2

class Usuario:
    def __init__(self, id, nombre, foto, cara):
        self.id = id
        self.nombre = nombre
        self.foto = foto
        self.cara = cara

class UsuarioDAO:
    def registrar_usuario(self, nombre, foto_bytes, cara_bytes):
        conn = DBConnection.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO usuarios (nombre, foto, cara) VALUES (%s, %s, %s)"
                # Use psycopg2.Binary for BYTEA
                cursor.execute(query, (nombre, psycopg2.Binary(foto_bytes), psycopg2.Binary(cara_bytes)))
                conn.commit()
                cursor.close()
                print("Usuario registrado exitosamente.")
            except Exception as e:
                print(f"Error al registrar usuario: {e}")
                conn.rollback()

    def obtener_todos(self):
        conn = DBConnection.get_connection()
        usuarios = []
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT id, nombre, foto, cara FROM usuarios"
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    # row[2] and row[3] are memoryview or bytes
                    usuarios.append(Usuario(row[0], row[1], row[2], row[3]))
                cursor.close()
            except Exception as e:
                print(f"Error al obtener usuarios: {e}")
        return usuarios
