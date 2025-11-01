# 🚀 INSTRUCCIONES DE DEPLOYMENT - AKIRA SASE

## ⚡ ACCIÓN INMEDIATA REQUERIDA

### 🔴 PASO 1: REVOCAR CREDENCIALES EXPUESTAS (CRÍTICO)

Las siguientes credenciales fueron detectadas en el repositorio y deben ser revocadas INMEDIATAMENTE:

#### OpenAI API Key
1. Ir a https://platform.openai.com/api-keys
2. Buscar la key que comienza con `sk-proj-yxuLub95kFNpxs16...`
3. Click en "Revoke" o "Delete"
4. Generar una nueva API key
5. Copiarla al archivo `.env`

#### Firebase Credentials
1. Ir a https://console.firebase.google.com
2. Seleccionar proyecto "akira-cyberwar"
3. Ir a Project Settings → Service Accounts
4. Click en "Generate New Private Key" para la cuenta `firebase-adminsdk-fbsvc@akira-cyberwar.iam.gserviceaccount.com`
5. Descargar el nuevo archivo JSON
6. Guardarlo como `firebase-credentials.json`
7. **Opcional**: Eliminar la cuenta de servicio antigua si no se usa en otro lugar

### 🟡 PASO 2: PREPARAR EL REPOSITORIO LOCAL

```bash
# 1. Asegurarse de estar en el directorio correcto
cd c:\Users\gatak\Desktop\akira

# 2. Verificar que los archivos sensibles NO estén en git
git status

# Si .env o firebase-credentials.json aparecen, eliminarlos:
git rm --cached .env
git rm --cached firebase-credentials.json
git rm --cached *.log

# 3. Verificar .gitignore
cat .gitignore | grep -E "\.env|firebase-credentials"

# 4. Copiar archivos de ejemplo y configurar
cp .env.example .env
nano .env  # Editar y añadir las NUEVAS credenciales

# 5. Generar secretos seguros
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(48))"
python -c "import secrets; print('API_SECRET_KEY=' + secrets.token_urlsafe(32))"
# Copiar estos valores al .env
```

### 🟢 PASO 3: DEPLOYMENT A GITHUB

#### Opción A: Script Automatizado (Recomendado)

**Windows:**
```cmd
deploy_to_github.bat
```

**Linux/Mac:**
```bash
chmod +x deploy_to_github.sh
./deploy_to_github.sh
```

#### Opción B: Manual

```bash
# 1. Inicializar git (si no está inicializado)
git init

# 2. Configurar remote
git remote add origin https://github.com/dajarony/akira.git

# 3. Agregar archivos
git add .

# 4. Verificar que NO se incluyan secretos
git status
# Asegurarse que .env y firebase-credentials.json NO aparezcan

# 5. Commit
git commit -m "Security hardening and CI/CD implementation - v2.0.0

- Implemented JWT authentication
- Added rate limiting
- Created target authorization system
- Enhanced security across all components
- Added comprehensive documentation
- Configured GitHub Actions CI/CD
"

# 6. Push
git push -u origin main

# Si falla (repositorio ya existe):
git pull --rebase origin main
git push -u origin main
```

### 🔵 PASO 4: CONFIGURAR GITHUB

1. **Ir al repositorio**: https://github.com/dajarony/akira

2. **Habilitar GitHub Actions**:
   - Settings → Actions → General
   - Permitir "Allow all actions and reusable workflows"
   - Save

3. **Configurar Secrets** (opcional, para CI/CD avanzado):
   - Settings → Secrets and variables → Actions
   - Añadir secrets (si necesario):
     - `SAFETY_API_KEY` (para dependency scanning)
     - Cualquier otro secret necesario para deployment

4. **Branch Protection** (recomendado):
   - Settings → Branches
   - Add rule for `main` branch
   - Enable:
     - ✅ Require pull request reviews
     - ✅ Require status checks to pass
     - ✅ Require branches to be up to date

5. **Verificar primer CI/CD run**:
   - Ir a Actions tab
   - Ver el workflow ejecutándose
   - Verificar que pase todos los checks

---

## 📋 CHECKLIST POST-DEPLOYMENT

### Seguridad
- [ ] Credenciales antiguas revocadas
- [ ] Nuevas credenciales generadas y configuradas
- [ ] `.env` NO está en el repositorio
- [ ] `firebase-credentials.json` NO está en el repositorio
- [ ] Secrets de GitHub configurados (si aplica)
- [ ] Branch protection activado

### Funcionalidad
- [ ] GitHub Actions ejecutándose correctamente
- [ ] Todos los tests pasando
- [ ] Security scans sin issues críticos
- [ ] Docker image building correctamente

### Documentación
- [ ] README.md actualizado
- [ ] SECURITY.md revisado
- [ ] DEPLOYMENT.md revisado
- [ ] CHANGELOG.md actualizado

---

## 🔍 VERIFICACIÓN

### 1. Verificar que NO hay secretos en el repositorio

```bash
# Clonar en un directorio temporal
cd /tmp
git clone https://github.com/dajarony/akira.git akira-test
cd akira-test

# Buscar patrones sospechosos
grep -r "sk-proj-" .
grep -r "-----BEGIN PRIVATE KEY-----" .
grep -r "firebase-adminsdk" .

# No debería haber resultados (excepto en archivos .example)
```

### 2. Verificar GitHub Actions

1. Ir a https://github.com/dajarony/akira/actions
2. Verificar que el workflow "Akira SASE CI/CD Pipeline" existe
3. Ver el último run y verificar que:
   - ✅ Security Scan pasó
   - ✅ Code Quality pasó
   - ✅ Unit Tests pasó
   - ✅ Build pasó

### 3. Verificar Documentación

1. Ver README en GitHub: https://github.com/dajarony/akira
2. Verificar que se muestra correctamente
3. Click en los links de documentación (SECURITY.md, DEPLOYMENT.md)

---

## 🚨 EN CASO DE PROBLEMAS

### Problema: "Credenciales siguen en el repositorio"

```bash
# Opción 1: Eliminar del historial con git filter-branch
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env firebase-credentials.json" \
  --prune-empty --tag-name-filter cat -- --all

# Opción 2: Usar BFG Repo-Cleaner (más rápido)
# Descargar de: https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --delete-files .env
java -jar bfg.jar --delete-files firebase-credentials.json
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Forzar push
git push --force --all
```

### Problema: "Push rechazado"

```bash
# Si el repositorio ya existe y tiene commits
git pull --rebase origin main

# Resolver conflictos si hay
git add .
git rebase --continue

# Push
git push -u origin main
```

### Problema: "GitHub Actions falla"

1. Ir a Actions tab
2. Click en el workflow fallido
3. Ver los logs para identificar el error
4. Común: dependencias faltantes
   - Verificar requirements.txt
   - Verificar que todos los imports existen

---

## 📞 SOPORTE

Si encuentras problemas durante el deployment:

1. **Revisar logs**: Ver el output del script/comando que falló
2. **Consultar documentación**:
   - SECURITY.md para problemas de seguridad
   - DEPLOYMENT.md para problemas de deployment
3. **GitHub Issues**: https://github.com/dajarony/akira/issues
4. **Security**: security@akira-cyber.com (para issues de seguridad)

---

## ✅ DEPLOYMENT COMPLETADO

Una vez que todos los pasos estén completos:

1. ✅ Credenciales revocadas y regeneradas
2. ✅ Repositorio limpio (sin secretos)
3. ✅ GitHub configurado correctamente
4. ✅ CI/CD ejecutándose
5. ✅ Verificaciones pasando

**¡Felicitaciones!** Akira SASE está ahora deployado de forma segura en GitHub con todas las mejoras de seguridad implementadas.

---

**Versión**: 2.0.0
**Última actualización**: 2025-01-01
**Creado por**: Akira Security Team
