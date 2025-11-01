# 🔌 **GUÍA DE INTEGRACIÓN BACKEND-FRONTEND**

## 🎯 **AKIRA SASE CYBERWAR MVP - INTEGRACIÓN COMPLETA**

Esta guía te ayudará a ejecutar Akira con integración real entre backend y frontend.

---

## 🚀 **OPCIÓN 1: INICIO AUTOMÁTICO (RECOMENDADO)**

### 📋 **Paso 1: Usar Script Integrado**
```bash
# Ejecutar script de inicio completo
python run_akira.py
```

**¿Qué hace este script?**
- ✅ Inicia backend en puerto 8000
- ✅ Inicia frontend en puerto 8080
- ✅ Verifica que ambos servicios estén funcionando
- ✅ Abre navegador automáticamente
- ✅ Maneja cierre limpio con Ctrl+C

---

## 🔧 **OPCIÓN 2: INICIO MANUAL**

### 📋 **Paso 1: Iniciar Backend**
```bash
# Terminal 1: Backend API
python main.py
```
**Resultado esperado:**
```
🚀 Akira SASE Cyberwar MVP starting up...
✅ Akira SASE Cyberwar MVP initialized successfully
🌐 API running on 0.0.0.0:8000
```

### 📋 **Paso 2: Iniciar Frontend**
```bash
# Terminal 2: Frontend UI
cd frontend
python -m http.server 8080 --bind 127.0.0.1
```
**Resultado esperado:**
```
Serving HTTP on 127.0.0.1 port 8080 (http://127.0.0.1:8080/) ...
```

### 📋 **Paso 3: Abrir Navegador**
```
http://localhost:8080
```

---

## 🧪 **VERIFICAR INTEGRACIÓN**

### 📋 **Paso 1: Test Automático**
```bash
# Ejecutar test de integración
python test_integration.py
```

**Resultado esperado:**
```
🧪 AKIRA INTEGRATION TEST
==================================================
🔧 Testing Backend Connection...
✅ Backend ping: OK
🔐 Testing Authenticated Endpoints...
✅ Authentication: OK
🌐 Testing Nmap Endpoint...
✅ Nmap endpoint: OK
🔍 Testing OSINT Endpoint...
✅ OSINT endpoint: OK
🎨 Testing Frontend Connection...
✅ Frontend accessible: OK
✅ Frontend content: OK

📊 TEST RESULTS:
==================================================
Backend Connection: ✅ OK
Authentication: ✅ OK
Nmap Endpoint: ✅ OK
OSINT Endpoint: ✅ OK
Frontend: ✅ OK

🎉 INTEGRATION TEST PASSED!
```

### 📋 **Paso 2: Test Manual en Navegador**

1. **Abrir**: http://localhost:8080
2. **Verificar**: Mensaje "Backend connected successfully" (verde)
3. **Probar**: Click en "Red Team" → Ingresar `127.0.0.1` → "START SCAN"
4. **Verificar**: Resultados reales del escaneo Nmap
5. **Probar**: Click en "Blue Team" → Ingresar IP → "BLOCK"
6. **Verificar**: IP bloqueada en firewall real

---

## 🎮 **FUNCIONALIDADES INTEGRADAS**

### 🔴 **Red Team (Ofensivo)**
| Función | Endpoint | Estado |
|---------|----------|--------|
| Nmap Scanner | `/offense/nmap` | ✅ Integrado |
| OSINT Collector | `/offense/osint` | ✅ Integrado |
| Exploit Launcher | `/offense/exploit` | ✅ Integrado |

### 🔵 **Blue Team (Defensivo)**
| Función | Endpoint | Estado |
|---------|----------|--------|
| Block IP | `/defense/firewall/block-ip` | ✅ Integrado |
| Deploy Honeypot | `/defense/honeypot/deploy/*` | ✅ Integrado |
| AI Log Analysis | `/defense/threat-detection/analyze` | ✅ Integrado |
| Defense Stats | `/defense/stats` | ✅ Integrado |

### 📊 **Dashboard**
| Métrica | Fuente | Estado |
|---------|--------|--------|
| Threat Overview | API Real | ✅ Integrado |
| Firewall Rules | API Real | ✅ Integrado |
| Honeypots Active | API Real | ✅ Integrado |
| AI Alerts | API Real | ✅ Integrado |

---

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### ❌ **Backend No Conecta**
```bash
# Verificar que el backend esté corriendo
curl http://localhost:8000/ping

# Si no responde, revisar logs:
python main.py
```

### ❌ **Frontend No Carga**
```bash
# Verificar que el frontend esté corriendo
curl http://localhost:8080

# Si no responde, reiniciar:
cd frontend
python -m http.server 8080
```

### ❌ **CORS Errors**
- El frontend ya está configurado con `mode: 'cors'`
- El backend tiene CORS habilitado para localhost
- Si persiste, verificar que ambos usen localhost (no 127.0.0.1 vs localhost)

### ❌ **Authentication Errors**
- Verificar que el token sea correcto: `akira-dev-token-2024`
- El token está configurado en `frontend/script.js`
- El backend valida este token en `main.py`

---

## 🎯 **CARACTERÍSTICAS DE LA INTEGRACIÓN**

### ✅ **Funcionalidades Reales**
- **Escaneos Nmap**: Ejecuta nmap real en el sistema
- **OSINT Collection**: Consultas DNS/WHOIS reales
- **Firewall Management**: Reglas de firewall reales (requiere permisos admin)
- **Honeypot Deployment**: Honeypots reales en puertos locales
- **AI Threat Detection**: Análisis real con patrones + IA
- **Real-time Updates**: Dashboard actualizado con datos reales

### ✅ **Fallback Inteligente**
- Si el backend no está disponible → Modo simulación
- Si una API falla → Fallback a simulación para esa función
- Notificaciones claras sobre el modo actual
- Sin interrupciones en la experiencia de usuario

### ✅ **Seguridad Integrada**
- Autenticación Bearer token
- Validación de inputs
- Restricciones éticas (IPs prohibidas)
- Logs de auditoría completos
- Manejo seguro de errores

---

## 🎉 **RESULTADO FINAL**

### 🛡️⚔️ **LO QUE TIENES AHORA:**

1. **Backend API Completa** - FastAPI con 25+ endpoints
2. **Frontend Profesional** - Interfaz cyberpunk interactiva
3. **Integración Real** - Comunicación bidireccional funcionando
4. **Fallback Inteligente** - Simulación cuando API no disponible
5. **Tests Automatizados** - Verificación de integración
6. **Scripts de Inicio** - Automatización completa
7. **Documentación Completa** - Guías y roadmap

### 🚀 **PRÓXIMOS PASOS:**

1. **Configurar APIs externas** (OpenAI, Firebase)
2. **Desplegar en producción** (Docker, cloud)
3. **Añadir más funcionalidades** (WebSockets, gráficos)
4. **Optimizar performance** (caching, CDN)

---

**🛡️⚔️ ¡Tu Akira SASE Cyberwar MVP está completamente integrado y funcionando! ⚔️🛡️**

Para cualquier problema, ejecuta `python test_integration.py` para diagnosticar.