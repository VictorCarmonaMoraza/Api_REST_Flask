FROM python:3.9.0
EXPOSE 5000
WORKDIR /app
RUN pip install Flask
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"] 


# FROM -->Version de python utilizada
# EXPOSE -->Puerto de Flask
# WORKDIR -->
# RUN -->El comando RUN se ejecuta cuando se está construyendo una imagen personalizada para realizar una acción
# COPY . .
# CMD -->Estamos diciendole a Docker que el comando que queremos ejecutar


# Comando para consola y crear imagen en docker : docker build -t rest-apis-flask-python .

# Levantar docker desde la terminal de comando: docker run -dp 5005:5000 rest-apis-flask-python