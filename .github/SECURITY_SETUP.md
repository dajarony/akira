# 🛡️ Configuración de Seguridad de GitHub

Este documento explica la configuración de seguridad implementada en el repositorio Akira SASE.

## ✅ Características de Seguridad Habilitadas

### 1. **CodeQL Analysis**
Workflow: `.github/workflows/codeql-analysis.yml`

- **Qué hace**: Analiza el código Python en busca de vulnerabilidades de seguridad
- **Cuándo se ejecuta**:
  - En cada push a `main` y `develop`
  - En cada pull request
  - Semanalmente los lunes a las 00:00 UTC
- **Resultados**: Se publican en la pestaña "Security" → "Code scanning alerts"

### 2. **Trivy Vulnerability Scanner**
Workflow: `.github/workflows/ci-cd.yml` (job: `security-scan`)

- **Qué hace**: Escanea el proyecto y dependencias en busca de vulnerabilidades conocidas (CVEs)
- **Severidad**: CRITICAL y HIGH
- **Resultados**: Se intentan subir a GitHub Security (requiere Code Scanning habilitado)

### 3. **TruffleHog Secret Scanning**
Workflow: `.github/workflows/ci-cd.yml` (job: `security-scan`)

- **Qué hace**: Detecta credenciales, tokens, y secretos accidentalmente incluidos en el código
- **Cuándo se ejecuta**: En cada push y pull request

### 4. **Dependabot**
Configuración: `.github/dependabot.yml`

- **Qué hace**: Monitorea dependencias y crea PRs automáticos para actualizaciones de seguridad
- **Ecosistemas monitoreados**:
  - Python (pip) - `requirements.txt`
  - GitHub Actions - workflows
  - Docker - Dockerfile
- **Frecuencia**: Semanal (lunes a las 09:00 UTC)

---

## 🚀 Activación Manual (Si es necesario)

Si los workflows fallan porque Code Scanning no está habilitado, sigue estos pasos:

### Opción 1: Habilitar desde la Interfaz Web

1. Ve a: https://github.com/dajarony/akira/settings/security_analysis
2. En "Code scanning", click en **"Set up"**
3. Selecciona **"Advanced"**
4. GitHub detectará el workflow de CodeQL existente
5. Click en **"Enable CodeQL"**

### Opción 2: Ejecutar el Workflow de CodeQL

1. Ve a: https://github.com/dajarony/akira/actions/workflows/codeql-analysis.yml
2. Click en **"Run workflow"**
3. Selecciona la rama `main`
4. Click en **"Run workflow"**

Esto habilitará automáticamente Code Scanning al ejecutarse por primera vez.

---

## 📊 Dónde Ver los Resultados

Una vez habilitado, podrás ver:

- **Code Scanning Alerts**: https://github.com/dajarony/akira/security/code-scanning
- **Dependabot Alerts**: https://github.com/dajarony/akira/security/dependabot
- **Secret Scanning**: https://github.com/dajarony/akira/security/secret-scanning
- **Security Overview**: https://github.com/dajarony/akira/security

---

## 🔧 Solución de Problemas

### Error: "Code scanning is not enabled"

**Solución**: Sigue los pasos de "Activación Manual" arriba.

El workflow está configurado con `continue-on-error: true` para que no falle mientras se habilita Code Scanning.

### Error: "Resource not accessible by integration"

**Solución**: Verifica que los permisos del workflow incluyan:
```yaml
permissions:
  contents: read
  security-events: write
  actions: read
```

Ya está configurado correctamente en este repositorio.

---

## 📝 Mantenimiento

### Actualizar Workflows

Los workflows se actualizan automáticamente gracias a Dependabot. Cuando hay una nueva versión de las actions, Dependabot creará un PR.

### Revisar Alertas

Se recomienda revisar las alertas de seguridad al menos semanalmente:

```bash
# Ver alertas con gh CLI
gh repo view dajarony/akira --web
# Navegar a: Security → Code scanning alerts
```

---

## 🎯 Políticas de Seguridad

Para más información sobre políticas de seguridad del proyecto, consulta:
- `docs/SECURITY.md` - Política de seguridad completa
- `docs/DEPLOYMENT.md` - Prácticas de despliegue seguro

---

**Última actualización**: 2025-11-05
**Mantenido por**: Claude AI Assistant para @dajarony
