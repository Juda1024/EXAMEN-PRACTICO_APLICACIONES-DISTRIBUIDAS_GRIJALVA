# Usamos Python sin instalar nada extra, porque socket y threading ya vienen incluidos.
FROM python:3.12-slim
WORKDIR /app
COPY servidor.py .
#CMD sirve para indicar el comando que se ejecutará al iniciar el contenedor. En este caso, ejecutamos el servidor de chat.
CMD ["python", "-u", "servidor.py"] 
