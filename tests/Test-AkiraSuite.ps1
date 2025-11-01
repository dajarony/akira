# Script de Pruebas Completo y Final para Akira SASE Cyberwar MVP

# --- Configuración ---
$HostUrl = "http://localhost:8000"
$Token = "akira-access-token-2025-MVP-cyberwar"
$headers = @{
    "Authorization" = "Bearer $Token"
    "Content-Type" = "application/json"
}

# --- Función de Prueba Reutilizable ---
function Run-Test {
    param (
        [string]$TestName,
        [scriptblock]$Command
    )
    Write-Host "===============================================================" -ForegroundColor Blue
    Write-Host "🧪 PRUEBA: $TestName" -ForegroundColor Yellow
    Write-Host "---------------------------------------------------------------" -ForegroundColor Blue
    
    try {
        Write-Host "▶️  Ejecutando..." -ForegroundColor Green
        $result = & $Command
        Write-Host "📋 Resultado:" -ForegroundColor White
        $result | ConvertTo-Json -Depth 5
        Write-Host ""
    } catch {
        Write-Host "❌ ERROR DURANTE LA PRUEBA:" -ForegroundColor Red
        $statusCode = $_.Exception.Response.StatusCode.Value__
        Write-Host "Status Code: $statusCode" -ForegroundColor Yellow
        try {
            $errorContent = $_.Exception.Response.GetResponseStream() | ForEach-Object { (New-Object System.IO.StreamReader($_)).ReadToEnd() }
            if ($errorContent) {
                Write-Host "Response Body: $errorContent" -ForegroundColor Red
            }
        } catch {
            Write-Host "Raw Error: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    
    Start-Sleep -Seconds 2
}

# --- Suite de Pruebas ---
Write-Host "🚀 INICIANDO SUITE DE PRUEBAS COMPLETA PARA AKIRA 🚀" -ForegroundColor Green

# 1. Status: Salud del Sistema
Run-Test "Salud del Sistema (/status/health)" {
    Invoke-RestMethod -Method Get -Uri "$HostUrl/status/health" -Headers $headers
}

# 2. Offense: Recolección OSINT
Run-Test "Recolección OSINT (/offense/osint)" {
    $body = @{ target_domain = "scanme.nmap.org"; sources = @("dns_records", "whois") } | ConvertTo-Json
    Invoke-RestMethod -Method Post -Uri "$HostUrl/offense/osint" -Headers $headers -Body $body
}

# 3. Offense: Escaneo Nmap (Simulado)
Run-Test "Escaneo Nmap - Simulado (/offense/nmap)" {
    $body = @{ target = @{ hostname = "scanme.nmap.org" }; ai_analysis = $false } | ConvertTo-Json
    Invoke-RestMethod -Method Post -Uri "$HostUrl/offense/nmap" -Headers $headers -Body $body
}

# 4. Defense: Desplegar un Honeypot
Run-Test "Desplegar Honeypot SSH (/defense/honeypot)" {
    $body = @{ honeypot_name = "final_test_ssh"; honeypot_type = "ssh"; port = 8025 } | ConvertTo-Json
    Invoke-RestMethod -Method Post -Uri "$HostUrl/defense/honeypot" -Headers $headers -Body $body
}

# 5. Defense: Crear una Regla de Firewall (Simulada)
Run-Test "Crear Regla de Firewall (/defense/firewall/rule)" {
    $body = @{ rule_name = "Final_Block_IP"; action = "drop"; source_ip = "8.8.4.4" } | ConvertTo-Json
    Invoke-RestMethod -Method Post -Uri "$HostUrl/defense/firewall/rule" -Headers $headers -Body $body
}

# 6. Defense: Obtener Estadísticas de Defensa
Run-Test "Estadísticas de Defensa (/defense/stats)" {
    Invoke-RestMethod -Method Get -Uri "$HostUrl/defense/stats" -Headers $headers
}

# 7. Limpieza: Eliminar Regla de Firewall
Write-Host "`n🧹 Iniciando limpieza de recursos creados..." -ForegroundColor Cyan
$rulesResponse = Invoke-RestMethod -Method Get -Uri "$HostUrl/defense/firewall/rules" -Headers $headers
$ruleId = ($rulesResponse.active_rules | Where-Object { $_.rule_name -eq "Final_Block_IP" }).rule_id
if ($ruleId) {
    Run-Test "Limpieza - Eliminar Regla de Firewall" {
        Invoke-RestMethod -Method Delete -Uri "$HostUrl/defense/firewall/rule/$ruleId" -Headers $headers
    }
} else {
    Write-Host "No se encontró el ID de la regla de firewall para limpiar (esto puede ser normal)." -ForegroundColor Yellow
}

# 8. Limpieza: Eliminar Honeypot
$honeypotsResponse = Invoke-RestMethod -Method Get -Uri "$HostUrl/defense/honeypots" -Headers $headers
$honeypotId = ($honeypotsResponse.active_honeypots | Where-Object { $_.honeypot_name -eq "final_test_ssh" }).honeypot_id
if ($honeypotId) {
    Run-Test "Limpieza - Detener Honeypot" {
        Invoke-RestMethod -Method Delete -Uri "$HostUrl/defense/honeypot/$honeypotId" -Headers $headers
    }
} else {
    Write-Host "No se encontró el ID del honeypot para limpiar (esto puede ser normal)." -ForegroundColor Yellow
}

Write-Host "`n✅ SUITE DE PRUEBAS FINALIZADA 🚀" -ForegroundColor Green
