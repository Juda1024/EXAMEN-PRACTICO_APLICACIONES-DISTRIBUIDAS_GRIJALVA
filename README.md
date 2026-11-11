# Chat en tiempo real con Python y Docker

Examen práctico de Aplicaciones Distribuidas.

Este proyecto permite que dos clientes y un servidor intercambien mensajes en tiempo real, sin esperar turnos. El servidor funciona dentro de Docker y los clientes en dos terminales de VS Code.

## Tecnologías utilizadas

- Python 3: `socket` para la comunicación TCP y `threading` para atender conexiones y recibir mensajes al mismo tiempo.
- Docker y Docker Compose: para ejecutar el servidor en un contenedor.
- No se necesitan librerías adicionales de Python.

## Archivos

- `servidor.py`: recibe las conexiones y distribuye los mensajes a ambos clientes. También permite escribir desde el servidor.
- `cliente.py`: se usa para los dos clientes, indicando el número al ejecutarlo.
- `Dockerfile`: indica cómo ejecutar el servidor en el contenedor.
- `docker-compose.yml`: configura el servidor, el puerto y la entrada de teclado.

## Requisitos

1. Tener instalado Python 3 en la computadora.
2. Tener Docker Desktop instalado y encendido (con Docker Compose disponible).
3. Abrir esta carpeta en Visual Studio Code.

## Cómo ejecutar

Abrir **tres terminales** en VS Code, todas ubicadas en la carpeta del proyecto.

### Terminal 1: servidor dentro de Docker

```bash
docker compose run --build --rm --service-ports servidor
```

El comando crea la imagen si es necesario y ejecuta el servidor en modo interactivo. **Se usa `--service-ports` para publicar el puerto 5000** y poder conectar los clientes desde Windows. Al dejar esta terminal abierta, también podemos escribir mensajes como SERVIDOR.

### Terminal 2: Cliente 1

```bash
python cliente.py 1
```

### Terminal 3: Cliente 2

```bash
python cliente.py 2
```

Si en Windows no funciona `python`, se puede probar `py cliente.py 1` y `py cliente.py 2`.

Los dos clientes se ejecutan directamente en la PC, no dentro de Docker. El servidor escucha en `0.0.0.0:5000` dentro del contenedor y los clientes se conectan a `127.0.0.1:5000` desde la PC.

### Otra forma: iniciar con `docker compose up`

```bash
docker compose up --build -d
docker compose attach servidor
```

El primer comando deja el contenedor encendido y el segundo conecta la terminal al servidor para poder escribir. Esta es una **alternativa**, no hay que ejecutar las dos formas al mismo tiempo. Para detener este modo, se escribe `salir` y después ejecuta `docker compose down`.

## Pruebas

1. Iniciar primero el servidor y después los dos clientes. Esperar a que el servidor muestre que los dos están conectados.
2. En Cliente 1 escribir `Hola a todos` y presionar Enter.
3. Verificar que en Cliente 1, Cliente 2 y el servidor aparezca `[CLIENTE 1]: Hola a todos`.
4. En Cliente 2 escribir `Buenos días` y comprobar que todos lo reciban como `[CLIENTE 2]: Buenos días`.
5. En la terminal del servidor escribir `Hola, clientes` y comprobar que los clientes reciban `[SERVIDOR]: Hola, clientes`.
6. Seguir enviando mensajes desde las tres terminales en cualquier orden para demostrar que no hay turnos.

Para cerrar, escribir `salir` en cada cliente y finalmente `salir` en el servidor.

## Docker Compose

El archivo `docker-compose.yml` debe permanecer junto al `Dockerfile` y `servidor.py`. No hace falta instalar Docker Compose como librería de Python: Docker Desktop ya incorpora el comando `docker compose` en instalaciones actuales.

Se recomienda `docker compose run` en lugar de iniciar el servidor en segundo plano con `up -d`, porque necesitamos poder escribir directamente desde la terminal del servidor.


