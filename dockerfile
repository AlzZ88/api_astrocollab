FROM python:3.11

# Instalar git
RUN apt-get update -y && apt-get install -y git

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de requerimientos y realizar la instalación
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copiar todo el contenido de tu aplicación al directorio de trabajo en el contenedor
COPY . .

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8000


# Comando para ejecutar la aplicación FastAPI utilizando uvicorn
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
