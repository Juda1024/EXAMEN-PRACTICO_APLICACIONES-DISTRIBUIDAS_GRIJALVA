import socket
import threading
import sys #sys se usa para leer argumentos de la línea de comandos.

HOST = "127.0.0.1"  # Docker publica el puerto en nuestra computadora.
PORT = 5000


def recibir(entrada):
    # Este hilo muestra los mensajes mientras seguimos escribiendo.
    try:
        for linea in entrada:
            print("\n" + linea.rstrip(), flush=True)
    except (OSError, UnicodeError):
        pass
    print("\nConexión con el servidor finalizada.", flush=True)


def main():
    # Usamos un solo archivo para Cliente 1 y Cliente 2.
    if len(sys.argv) != 2 or sys.argv[1] not in ("1", "2"):
        print("Uso: python cliente.py 1  (o python cliente.py 2)")
        return

    # Creamos el socket del cliente y nos conectamos al servidor.
    nombre = "CLIENTE " + sys.argv[1]
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((HOST, PORT))
        # Enviamos el nombre y esperamos a que el servidor lo acepte.
        cliente.sendall((nombre + "\n").encode("utf-8"))
        entrada = cliente.makefile("r", encoding="utf-8")
        respuesta = entrada.readline().strip()

        if respuesta != "OK":
            print(respuesta or "El servidor cerró la conexión.")
            return

        print(f"Conectado como {nombre}. Escribe 'salir' para terminar.")
        threading.Thread(target=recibir, args=(entrada,), daemon=True).start()

        # Enviamos mensajes al servidor.
        while True:
            mensaje = input(f"{nombre} > ").strip()
            if mensaje.lower() == "salir":
                break
            if mensaje:
                cliente.sendall((mensaje + "\n").encode("utf-8"))

    except ConnectionRefusedError:
        print("No se pudo conectar. Comprueba que Docker esté ejecutando el servidor.")
    except (OSError, KeyboardInterrupt, EOFError):
        print("\nCliente desconectado.")
    finally:
        # Shutdown también permite que termine el hilo que recibe mensajes.
        try:
            cliente.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        cliente.close()


if __name__ == "__main__":
    main()
