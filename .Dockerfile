# Imagen base oficial de Python (azure app service custom container)
#https://learn.microsoft.com/en-us/azure/app-service/tutorial-custom-container?tabs=azure-cli&pivots=container-linux
#https://learn.microsoft.com/es-es/azure/devops/pipelines/apps/cd/deploy-docker-webapp?view=azure-devops&tabs=java%2Cyaml
FROM python:3.13-slim

# Instala dependencias del sistema necesarias para pyodbc y SQL Server
RUN apt-get update && \
    apt-get install -y gcc g++ unixodbc-dev curl gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /

COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto para Flask
EXPOSE 5000

# Variable de entorno para producción
ENV ENVIRONMENT_FLAG=prod

# Comando para ejecutar la aplicación usando gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]