# Usamos Python sin instalar nada extra, porque socket y threading ya vienen incluidos.
FROM python:3.12-slim
# Copiamos el archivo del cliente al contenedor.
WORKDIR /app
# Copiamos el archivo del servidor al contenedor.
COPY servidor.py . 
#CMD sirve para indicar el comando que se ejecutará al iniciar el contenedor. En este caso, ejecutamos el servidor de chat.
CMD ["python", "-u", "servidor.py"] 
