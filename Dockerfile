# Etapa de construcción
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requerimientos y el código fuente
COPY requirements.txt requirements.txt
COPY . .

# Instalar las dependencias
RUN pip install -r requirements.txt

# Exponer el puerto que la aplicación utilizará
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
