# 🛡️⚔️ Akira SASE Cyberwar MVP

## Sistema Híbrido de Ciberseguridad Ofensiva y Defensiva

**Arquitectura SUME + STDG** - Sistema modular para operaciones de ciberseguridad éticas con capacidades ofensivas y defensivas integradas.

---

## 📋 Tabla de Contenidos

- [🎯 Características Principales](#-características-principales)
- [🏗️ Arquitectura](#️-arquitectura)
- [🚀 Instalación Rápida](#-instalación-rápida)
- [⚙️ Configuración](#️-configuración)
- [📖 Uso](#-uso)
- [🔌 API Endpoints](#-api-endpoints)
- [🧪 Testing](#-testing)
- [🐳 Docker](#-docker)
- [🔒 Seguridad](#-seguridad)
- [🤝 Contribución](#-contribución)
- [📄 Licencia](#-licencia)

---

## 🎯 Características Principales

### 🔴 Operaciones Ofensivas
- **🌐 Escaneo Nmap**: Escaneos de red completos con análisis IA
- **🔍 Recolección OSINT**: Inteligencia de fuentes abiertas automatizada
- **⚡ Exploits Éticos**: Verificación de vulnerabilidades controlada y segura

### 🔵 Operaciones Defensivas
- **🛡️ Gestión Firewall**: Reglas automáticas y bloqueo de amenazas
- **🍯 Honeypots**: Señuelos inteligentes SSH/HTTP/FTP para detectar atacantes
- **🤖 Detección IA**: Análisis de amenazas con OpenAI GPT-4

### 📊 Monitoreo y Control
- **💚 Estado del Sistema**: Salud de servicios y recursos en tiempo real
- **📝 Logs Centralizados**: Auditoría completa de actividades
- **📈 Estadísticas**: Métricas de seguridad y dashboards

---

## 🏗️ Arquitectura

```
Akira SASE Cyberwar MVP
├── 🔴 Módulos Ofensivos
│   ├── Nmap Scanner (Escaneo de red)
│   ├── OSINT Collector (Inteligencia)
│   └── Exploit Launcher (Verificación ética)
├── 🔵 Módulos Defensivos
│   ├── Firewall Manager (Gestión automática)
│   ├── Honeypot Deployer (Señuelos inteligentes)
│   └── AI Threat Detector (Detección con IA)
├── 🧠 Servicios Core
│   ├── OpenAI Integration (GPT-4)
│   ├── Firebase Integration (Almacenamiento)
│   └── Logging System (Auditoría)
└── 🌐 API REST
    ├── FastAPI (Framework)
    ├── Authentication (Bearer Token)
    └── Documentation (Swagger)
```

### Principios de Diseño

- **SUME**: Sistemas Unificados Modulares Escalables
- **STDG**: Seguridad, Transparencia, Documentación, Gobernanza
- **Ético**: Solo para uso autorizado y educativo
- **Modular**: Componentes independientes y reutilizables
- **Escalable**: Arquitectura preparada para crecimiento

---

## 🚀 Instalación Rápida

### Opción 1: Script Automático (Recomendado)

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/akira-sase-cyberwar-mvp.git
cd akira-sase-cyberwar-mvp

# Ejecutar script de despliegue
python deploy.py
```

### Opción 2: Instalación Manual

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 4. Ejecutar aplicación
python main.py
```

### Requisitos del Sistema

- **Python**: 3.8+
- **Sistema Operativo**: Windows, Linux, macOS
- **RAM**: 2GB mínimo, 4GB recomendado
- **Espacio**: 1GB libre
- **Red**: Acceso a internet para APIs

---

## ⚙️ Configuración

### Variables de Entorno (.env)

```bash
# Configuración de Entorno
ENVIRONMENT=development
LOG_LEVEL=INFO

# API
API_HOST=0.0.0.0
API_PORT=8000
API_ACCESS_TOKEN=tu-token-seguro-aqui

# OpenAI (REQUERIDO)
OPENAI_API_KEY=sk-proj-tu-clave-aqui
OPENAI_MODEL=gpt-4

# Firebase (REQUERIDO)
FIREBASE_PROJECT_ID=tu-proyecto-firebase
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

# Características
ENABLE_AI_ANALYSIS=true
ENABLE_NMAP_SCANNING=true
ENABLE_FIREWALL_MANAGEMENT=true
```

### Configuración de Firebase

1. Crear proyecto en [Firebase Console](https://console.firebase.google.com)
2. Generar clave de servicio (Service Account Key)
3. Descargar `firebase-credentials.json`
4. Colocar en directorio raíz del proyecto

### Configuración de OpenAI

1. Crear cuenta en [OpenAI Platform](https://platform.openai.com)
2. Generar API key
3. Configurar en variable `OPENAI_API_KEY`

---

## 📖 Uso

### Iniciar el Sistema

```bash
# Activar entorno virtual
source venv/bin/activate

# Iniciar servidor
python main.py
```

### Acceder a la API

- **API Base**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/ping

### Ejemplos de Uso

#### 1. Escaneo Nmap

```bash
curl -X POST "http://localhost:8000/offense/nmap" \
  -H "Authorization: Bearer tu-token" \
  -H "Content-Type: application/json" \
  -d '{
    "target": "192.168.1.1",
    "scan_type": "basic",
    "port_range": "80,443,22",
    "ai_analysis": true
  }'
```

#### 2. Recolección OSINT

```bash
curl -X POST "http://localhost:8000/offense/osint" \
  -H "Authorization: Bearer tu-token" \
  -H "Content-Type: application/json" \
  -d '{
    "target": "example.com",
    "osint_type": "domain",
    "sources": ["dns", "whois"],
    "ai_analysis": true
  }'
```

#### 3. Desplegar Honeypot

```bash
curl -X POST "http://localhost:8000/defense/honeypot/deploy/ssh" \
  -H "Authorization: Bearer tu-token" \
  -H "Content-Type: application/json" \
  -d '{
    "port": 2222,
    "interface": "0.0.0.0"
  }'
```

#### 4. Análisis de Amenazas

```bash
curl -X POST "http://localhost:8000/defense/threat-detection/analyze" \
  -H "Authorization: Bearer tu-token" \
  -H "Content-Type: application/json" \
  -d '{
    "log_entries": [
      "Failed password for root from 192.168.1.100 port 22 ssh2",
      "Failed password for admin from 192.168.1.100 port 22 ssh2"
    ],
    "source": "ssh_server"
  }'
```

---

## 🔌 API Endpoints

### 🔴 Endpoints Ofensivos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/offense/nmap` | Ejecutar escaneo Nmap |
| POST | `/offense/osint` | Recolección OSINT |
| GET | `/offense/exploits` | Listar exploits disponibles |
| POST | `/offense/exploit` | Ejecutar exploit ético |

### 🔵 Endpoints Defensivos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/defense/firewall/status` | Estado del firewall |
| POST | `/defense/firewall/block-ip` | Bloquear IP maliciosa |
| POST | `/defense/honeypot/deploy/ssh` | Desplegar honeypot SSH |
| GET | `/defense/honeypot/status` | Estado de honeypots |
| POST | `/defense/threat-detection/analyze` | Analizar logs |
| GET | `/defense/stats` | Estadísticas defensivas |

### 📊 Endpoints de Estado

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/status/health` | Salud del sistema |
| GET | `/status/system` | Información del sistema |
| GET | `/ping` | Health check simple |

---

## 🧪 Testing

### Tests Automatizados

```bash
# Test completo de la API
python test_complete_api.py

# Tests individuales
python test_nmap_scanner.py
python test_osint_collector.py
python test_firewall_manager.py
python test_honeypot_deployer.py
python test_ai_threat_detector.py
```

### Tests Manuales

```bash
# Verificar endpoints básicos
curl http://localhost:8000/ping

# Test con autenticación
curl -H "Authorization: Bearer tu-token" \
     http://localhost:8000/status/health
```

---

## 🐳 Docker

### Construcción y Ejecución

```bash
# Construir imagen
docker-compose build

# Ejecutar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f akira

# Detener servicios
docker-compose down
```

### Configuración Docker

El archivo `docker-compose.yml` incluye:
- **Akira API**: Servicio principal
- **Redis**: Cache (opcional)
- **PostgreSQL**: Base de datos (opcional)

---

## 🔒 Seguridad

### Consideraciones de Seguridad

1. **Autenticación**: Usar tokens seguros y únicos
2. **HTTPS**: Implementar TLS en producción
3. **Firewall**: Restringir acceso a IPs autorizadas
4. **Logs**: Monitorear actividad sospechosa
5. **Updates**: Mantener dependencias actualizadas

### Uso Ético

⚠️ **IMPORTANTE**: Este sistema está diseñado exclusivamente para:

- ✅ Pruebas de penetración autorizadas
- ✅ Auditorías de seguridad internas
- ✅ Investigación de ciberseguridad ética
- ✅ Entrenamiento y educación

❌ **NUNCA usar contra sistemas sin autorización explícita**

### Responsabilidad Legal

El uso de este software es responsabilidad del usuario. Los desarrolladores no se hacen responsables del uso indebido o ilegal de esta herramienta.

---

## 🤝 Contribución

### Cómo Contribuir

1. **Fork** el repositorio
2. **Crear** rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Crear** Pull Request

### Estándares de Código

- **Python**: PEP 8
- **Documentación**: Docstrings en español
- **Tests**: Cobertura mínima 80%
- **Commits**: Mensajes descriptivos

### Roadmap de Desarrollo

Ver [ROADMAP.md](ROADMAP.md) para funcionalidades planificadas.

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

### Términos de Uso

- ✅ Uso comercial permitido
- ✅ Modificación permitida
- ✅ Distribución permitida
- ✅ Uso privado permitido
- ⚠️ Sin garantía
- ⚠️ Limitación de responsabilidad

---

## 📞 Soporte

### Contacto

- **Email**: security@akira-cyber.com
- **Issues**: [GitHub Issues](https://github.com/tu-usuario/akira-sase-cyberwar-mvp/issues)
- **Documentación**: [Wiki](https://github.com/tu-usuario/akira-sase-cyberwar-mvp/wiki)

### FAQ

**P: ¿Necesito permisos especiales para usar Akira?**
R: Sí, algunas funciones como gestión de firewall requieren permisos administrativos.

**P: ¿Funciona en Windows?**
R: Sí, Akira es compatible con Windows, Linux y macOS.

**P: ¿Es gratuito?**
R: Sí, Akira es open source bajo licencia MIT.

**P: ¿Puedo usar Akira en producción?**
R: Este es un MVP. Para producción, se recomienda auditoría de seguridad adicional.

---

## 🙏 Agradecimientos

- **OpenAI**: Por la API de GPT-4
- **Firebase**: Por los servicios de backend
- **FastAPI**: Por el framework web
- **Nmap**: Por las capacidades de escaneo
- **Comunidad Python**: Por las librerías utilizadas

---

**🛡️⚔️ Akira SASE Cyberwar MVP - Ciberseguridad Ética para un Mundo Digital Seguro ⚔️🛡️**

---

*Última actualización: Julio 2025*