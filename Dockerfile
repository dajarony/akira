# Akira SASE Cyberwar MVP - Docker Container
FROM python:3.11-slim

# Metadata
LABEL maintainer="Akira Security Team <security@akira-cyber.com>"
LABEL version="1.0.0-MVP"
LABEL description="Akira SASE Cyberwar MVP - Sistema híbrido de ciberseguridad"

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Crear usuario no-root para seguridad
RUN groupadd -r akira && useradd -r -g akira akira

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    wget \
    nmap \
    dnsutils \
    net-tools \
    iputils-ping \
    iptables \
    ufw \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para cache de Docker)
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p logs mapa-global cambios && \
    touch akira.log

# Establecer permisos
RUN chown -R akira:akira /app

# Cambiar a usuario no-root
USER akira

# Exponer puerto
EXPOSE 8000

# Variables de entorno por defecto
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV ENVIRONMENT=production
ENV DEBUG=false
ENV LOG_LEVEL=INFO

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ping || exit 1

# Comando por defecto
CMD ["python", "main.py"]

# Metadata adicional
LABEL org.opencontainers.image.title="Akira SASE Cyberwar MVP"
LABEL org.opencontainers.image.description="Sistema modular de ciberseguridad ofensiva y defensiva"
LABEL org.opencontainers.image.version="1.0.0-MVP"
LABEL org.opencontainers.image.authors="Auralis Security Team"
LABEL org.opencontainers.image.source="https://github.com/akira-cyber/akira-sase"
LABEL org.opencontainers.image.documentation="https://docs.akira-cyber.com"
