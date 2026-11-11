import socket
import threading

HOST = "0.0.0.0"  # Aceptamos conexiones desde fuera del contenedor.
PORT = 5000

clientes = {}  # Guardamos la conexión de cada cliente y su nombre.
candado = threading.Lock() #Evitamos que dos hilos accedan a la lista de clientes al mismo tiempo.
activo = threading.Event() #activo es un evento que indica si el servidor está activo o no.
activo.set()

#Funcion para enviar un mensaje a todos los clientes conectados.
def enviar_a_todos(mensaje):
    # Copiamos las conexiones para no bloquear la llegada de otros clientes.
    with candado:
        conexiones = list(clientes.keys())
    # Enviamos el mensaje a todos los clientes conectados.
    for conexion in conexiones:
        try:
            conexion.sendall((mensaje + "\n").encode("utf-8"))
        except OSError:
            pass

#Función que atiende a un cliente en un hilo separado.
def atender_cliente(conexion, direccion):
    nombre = None
    try:
        # Abrimos un archivo de texto para leer las líneas que envía el cliente.
        with conexion:
            with conexion.makefile("r", encoding="utf-8") as entrada:
                # El primer dato que recibimos es el nombre del cliente.
                nombre = entrada.readline().strip().upper()

                #comprobamos si el cliente es permitido y si ya hay dos clientes conectados.
                #candado se usa para evitar que dos hilos accedan a la lista de clientes al mismo tiempo.
                with candado:
                    permitido = (nombre in ("CLIENTE 1", "CLIENTE 2")
                                 and nombre not in clientes.values()
                                 and len(clientes) < 2)
                    if permitido:
                        clientes[conexion] = nombre

                if not permitido:
                    conexion.sendall(b"ERROR: cliente no permitido o ya conectado.\n")
                    return

                # Confirmamos la conexión antes de mostrarla en el cliente.
                conexion.sendall(b"OK\n")
                print(f"\n{nombre} conectado desde {direccion}", flush=True)
                enviar_a_todos(f"[SERVIDOR]: {nombre} se ha conectado.")

                # Cada cliente tiene su hilo, así que todos pueden escribir a la vez.
                for linea in entrada:
                    mensaje = linea.strip()
                    if mensaje.lower() == "salir":
                        break
                    if mensaje:
                        texto = f"[{nombre}]: {mensaje}"
                        print("\n" + texto, flush=True)
                        enviar_a_todos(texto)

    except (OSError, UnicodeError):
        pass
    # Cuando el cliente se desconecta, lo eliminamos de la lista y avisamos a los demás.
    finally:
        with candado:
            conectado = conexion in clientes
            clientes.pop(conexion, None)
        if conectado:
            print(f"\n{nombre} se ha desconectado.", flush=True)
            enviar_a_todos(f"[SERVIDOR]: {nombre} se ha desconectado.")


def escribir_servidor():
    # Este hilo permite escribir desde Docker sin detener las conexiones.
    while activo.is_set():
        try:
            mensaje = input("SERVIDOR > ").strip()
        except (EOFError, KeyboardInterrupt):
            activo.clear()
            break
        # Si escribimos 'salir', cerramos el servidor y todas las conexiones.
        if mensaje.lower() == "salir":
            activo.clear()
            break
        if mensaje:
            texto = f"[SERVIDOR]: {mensaje}"
            print("\n" + texto, flush=True)
            enviar_a_todos(texto)


def main():
    # Creamos el socket del servidor y lo ponemos a escuchar.
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen(2)
    servidor.settimeout(0.5)  # Permite revisar si escribimos 'salir'.

    print(f"Servidor de chat escuchando en el puerto {PORT}", flush=True)
    print("Esperando a CLIENTE 1 y CLIENTE 2...", flush=True)
    print("Escribe 'salir' para cerrar el servidor.\n", flush=True)

    # El servidor recibe conexiones en el hilo principal.
    threading.Thread(target=escribir_servidor, daemon=True).start()

    try:
        # El bucle principal acepta conexiones y crea un hilo para cada cliente.
        while activo.is_set():
            try:
                conexion, direccion = servidor.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            threading.Thread(target=atender_cliente,
                             args=(conexion, direccion), daemon=True).start()
    except KeyboardInterrupt:
        pass
    # Cerramos el servidor y todas las conexiones de clientes.
    finally:
        activo.clear()
        servidor.close()
        with candado:
            conexiones = list(clientes.keys())
        for conexion in conexiones:
            try:
                conexion.shutdown(socket.SHUT_RDWR)
                conexion.close()
            except OSError:
                pass
        print("\nServidor cerrado.", flush=True)

if __name__ == "__main__":
    main()
