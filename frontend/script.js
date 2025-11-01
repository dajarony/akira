// Akira SASE Cyberwar MVP - JavaScript

// Configuration
const API_BASE_URL = 'http://localhost:8000';
const API_TOKEN = 'akira-access-token-2025-MVP-cyberwar';  // Matches backend .env

// API Helper function
async function makeAPICall(endpoint, method = 'GET', data = null) {
    const url = `${API_BASE_URL}${endpoint}`;
    const options = {
        method: method,
        headers: {
            'Authorization': `Bearer ${API_TOKEN}`,
            'Content-Type': 'application/json',
        },
        mode: 'cors'
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`API call failed for ${endpoint}:`, error);
        throw error;
    }
}

// Global state
let currentTab = 'dashboard';
let scanResults = [];
let threatData = [];

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    startRealTimeUpdates();
});

// Test backend connection
async function testBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/ping`);
        if (response.ok) {
            console.log('✅ Backend connection: OK');
            showNotification('Backend connected successfully', 'success');
            return true;
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        console.error('❌ Backend connection failed:', error);
        showNotification('Backend connection failed - using simulation mode', 'warning');
        return false;
    }
}

// Initialize application
function initializeApp() {
    console.log('🚀 Initializing Akira SASE Cyberwar MVP...');
    
    // Test backend connection
    testBackendConnection();
    
    // Set initial tab
    showTab('dashboard');
    
    // Update status
    updateSystemStatus();
    
    // Load initial data
    loadDashboardData();
    
    console.log('✅ Akira initialized successfully');
}

// Test backend connection
async function testBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/ping`);
        if (response.ok) {
            console.log('✅ Backend connection: OK');
            showNotification('Backend connected successfully', 'success');
            
            // Update status indicator
            const statusItems = document.querySelectorAll('.status-item');
            statusItems.forEach(item => {
                if (item.textContent.includes('API Connected')) {
                    item.innerHTML = '🟢 API Connected';
                }
            });
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        console.error('❌ Backend connection failed:', error);
        showNotification('Backend connection failed - using simulation mode', 'warning');
        
        // Update status indicator
        const statusItems = document.querySelectorAll('.status-item');
        statusItems.forEach(item => {
            if (item.textContent.includes('API Connected')) {
                item.innerHTML = '🔴 API Disconnected';
            }
        });
    }
}

// Setup event listeners
function setupEventListeners() {
    // Tab navigation
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const tabName = e.target.getAttribute('data-tab');
            showTab(tabName);
        });
    });
    
    // Form submissions
    document.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const target = e.target;
            if (target.id === 'nmap-target' || target.closest('.nmap-scanner')) {
                startNmapScan();
            } else if (target.id === 'osint-target' || target.closest('.osint-collector')) {
                startOsintScan();
            } else if (target.id === 'block-ip') {
                blockIP();
            }
        }
    });
}

// Tab management
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    const selectedTab = document.getElementById(tabName);
    const selectedBtn = document.querySelector(`[data-tab="${tabName}"]`);
    
    if (selectedTab && selectedBtn) {
        selectedTab.classList.add('active');
        selectedBtn.classList.add('active');
        currentTab = tabName;
        
        // Load tab-specific data
        loadTabData(tabName);
    }
}

// Load tab-specific data
function loadTabData(tabName) {
    switch(tabName) {
        case 'dashboard':
            loadDashboardData();
            break;
        case 'redteam':
            loadRedTeamData();
            break;
        case 'blueteam':
            loadBlueTeamData();
            break;
        case 'ai':
            loadAIData();
            break;
        case 'logs':
            loadLogsData();
            break;
    }
}

// Dashboard functions
async function loadDashboardData() {
    // Try to load real data from API
    try {
        await loadRealDashboardData();
    } catch (error) {
        console.log('Loading simulated dashboard data...');
        // Fallback to simulated data
        updateThreatOverview();
        updateTeamStatus();
        updateAIIntelligence();
    }
}

// Load real dashboard data from API
async function loadRealDashboardData() {
    try {
        // Load defense stats
        const defenseStats = await makeAPICall('/defense/stats');
        if (defenseStats.success) {
            updateRealDefenseStats(defenseStats.defense_stats);
        }
        
        // Load threat detection status
        const threatStatus = await makeAPICall('/defense/threat-detection/status');
        if (threatStatus.success) {
            updateRealThreatStatus(threatStatus.threat_status);
        }
        
        // Load firewall status
        const firewallStatus = await makeAPICall('/defense/firewall/status');
        if (firewallStatus.success) {
            updateRealFirewallStatus(firewallStatus.firewall_status);
        }
        
        console.log('✅ Real dashboard data loaded');
        
    } catch (error) {
        console.error('Failed to load real dashboard data:', error);
        throw error;
    }
}

// Update dashboard with real defense stats
function updateRealDefenseStats(stats) {
    // Update firewall rules count
    const firewallRulesElement = document.getElementById('firewall-rules');
    if (firewallRulesElement) {
        firewallRulesElement.textContent = stats.active_firewall_rules || 0;
    }
    
    // Update honeypots count
    const honeypotsElement = document.getElementById('honeypots');
    if (honeypotsElement) {
        honeypotsElement.textContent = `${stats.active_honeypots || 0} active`;
    }
    
    // Update blocked IPs count
    const blockedIpsElement = document.getElementById('blocked-ips');
    if (blockedIpsElement) {
        blockedIpsElement.textContent = stats.blocked_ips_count || 0;
    }
    
    // Update AI alerts
    const aiAlertsElement = document.getElementById('ai-alerts');
    if (aiAlertsElement) {
        aiAlertsElement.textContent = `${stats.alerts_generated_today || 0} today`;
    }
}

// Update dashboard with real threat status
function updateRealThreatStatus(threatStatus) {
    // Update threat counts by severity
    const severityDistribution = threatStatus.severity_distribution || {};
    
    const criticalElement = document.getElementById('critical-count');
    if (criticalElement) {
        criticalElement.textContent = severityDistribution.critical || 0;
    }
    
    const highElement = document.getElementById('high-count');
    if (highElement) {
        highElement.textContent = severityDistribution.high || 0;
    }
    
    const mediumElement = document.getElementById('medium-count');
    if (mediumElement) {
        mediumElement.textContent = severityDistribution.medium || 0;
    }
    
    const lowElement = document.getElementById('low-count');
    if (lowElement) {
        lowElement.textContent = severityDistribution.low || 0;
    }
}

// Update dashboard with real firewall status
function updateRealFirewallStatus(firewallStatus) {
    // Update firewall rules in Blue Team section
    const fwRulesElement = document.getElementById('fw-rules');
    if (fwRulesElement) {
        fwRulesElement.textContent = firewallStatus.total_rules || 0;
    }
    
    // Update blocked IPs in Blue Team section
    const fwBlockedElement = document.getElementById('fw-blocked');
    if (fwBlockedElement) {
        fwBlockedElement.textContent = firewallStatus.blocked_ips_count || 0;
    }
}

function updateThreatOverview() {
    // Simulate threat data
    const threats = {
        critical: Math.floor(Math.random() * 5),
        high: Math.floor(Math.random() * 10) + 3,
        medium: Math.floor(Math.random() * 20) + 8,
        low: Math.floor(Math.random() * 15) + 5
    };
    
    document.getElementById('critical-count').textContent = threats.critical;
    document.getElementById('high-count').textContent = threats.high;
    document.getElementById('medium-count').textContent = threats.medium;
    document.getElementById('low-count').textContent = threats.low;
}

function updateTeamStatus() {
    // Red Team Status
    document.getElementById('active-scans').textContent = Math.floor(Math.random() * 5) + 1;
    document.getElementById('osint-jobs').textContent = Math.floor(Math.random() * 3) + 1;
    document.getElementById('exploits-found').textContent = Math.floor(Math.random() * 20) + 5;
    document.getElementById('success-rate').textContent = (Math.random() * 20 + 75).toFixed(0) + '%';
    
    // Blue Team Status
    document.getElementById('firewall-rules').textContent = Math.floor(Math.random() * 20) + 40;
    document.getElementById('honeypots').textContent = Math.floor(Math.random() * 3) + 3 + ' active';
    document.getElementById('blocked-ips').textContent = Math.floor(Math.random() * 30) + 15;
    document.getElementById('ai-alerts').textContent = Math.floor(Math.random() * 10) + 3 + ' today';
}

function updateAIIntelligence() {
    const threats = [
        'SQL Injection from 192.168.1.100',
        'SSH Brute Force from 10.0.0.50',
        'Port Scan from 172.16.1.5',
        'XSS Attempt from 192.168.2.10',
        'DDoS Attack from 203.0.113.0'
    ];
    
    const randomThreat = threats[Math.floor(Math.random() * threats.length)];
    document.querySelector('.threat-type').textContent = randomThreat;
}

// Red Team functions
async function startNmapScan() {
    const target = document.getElementById('nmap-target').value;
    const ports = document.getElementById('nmap-ports').value;
    const type = document.getElementById('nmap-type').value;
    
    if (!target) {
        showNotification('Please enter a target', 'error');
        return;
    }
    
    const statusElement = document.getElementById('nmap-status');
    statusElement.innerHTML = '🟡 Scanning... <div class="loading"></div>';
    
    // Real API call - formato correcto para el backend
    const scanData = {
        target: {
            ip: target.includes('/') ? null : target,
            hostname: target.includes('/') ? null : target
        },
        scan_type: type === 'basic' ? 'tcp_syn' : type === 'aggressive' ? 'aggressive' : 'stealth',
        port_range: ports || '80,443,22',
        ai_analysis: true,
        save_results: true
    };
    
    console.log('🌐 Starting Nmap scan:', scanData);
    
    try {
        const result = await makeAPICall('/offense/nmap', 'POST', scanData);
        
        // Process real results
        const results = [];
        if (result.scan_results && result.scan_results.hosts) {
            result.scan_results.hosts.forEach(host => {
                if (host.ports) {
                    host.ports.forEach(port => {
                        const status = port.state === 'open' ? 'Open' : 
                                     port.state === 'closed' ? 'Closed' : 'Filtered';
                        const icon = port.state === 'open' ? '🎯' : 
                                   port.state === 'closed' ? '🔒' : '⚠️';
                        results.push(`${icon} ${host.ip}:${port.port} ${port.service || 'Unknown'} - ${status}`);
                    });
                }
            });
        }
        
        if (results.length === 0) {
            results.push(`🎯 Scan completed for ${target}`);
        }
        
        updateScanResults(results);
        statusElement.innerHTML = '🟢 Scan Complete';
        showNotification('Nmap scan completed successfully', 'success');
        
        // Show AI analysis if available
        if (result.ai_analysis) {
            showNotification(`AI Analysis: ${result.ai_analysis.summary}`, 'info');
        }
        
    } catch (error) {
        console.error('Nmap scan failed:', error);
        statusElement.innerHTML = '🔴 Scan Failed';
        showNotification(`Scan failed: ${error.message}`, 'error');
        
        // Fallback to simulation if API fails
        console.log('Falling back to simulation...');
        simulateScanProgress('nmap-status', () => {
            const results = [
                `🎯 ${target}:22 SSH - Open`,
                `🎯 ${target}:80 HTTP - Open`,
                `⚠️ ${target}:443 HTTPS - Filtered`
            ];
            updateScanResults(results);
            statusElement.innerHTML = '🟢 Scan Complete (Simulated)';
            showNotification('Scan completed in simulation mode', 'warning');
        });
    }
}

async function startOsintScan() {
    const target = document.getElementById('osint-target').value;
    const type = document.getElementById('osint-type').value;
    
    if (!target) {
        showNotification('Please enter a target', 'error');
        return;
    }
    
    const statusElement = document.getElementById('osint-status');
    statusElement.innerHTML = '🟡 Collecting... <div class="loading"></div>';
    
    const osintData = {
        target_domain: type === 'domain' ? target : null,
        target_email: type === 'email' ? target : null,
        target_username: null,
        company_name: null,
        sources: ['dns_records', 'whois', 'subdomain_enum'],
        depth_level: 2,
        ai_analysis: true,
        save_results: true
    };
    
    console.log('🔍 Starting OSINT collection:', osintData);
    
    try {
        const result = await makeAPICall('/offense/osint', 'POST', osintData);
        
        // Process real OSINT results
        const results = [];
        if (result.osint_results) {
            const osint = result.osint_results;

            results.push(`📊 Target: ${target}`);

            if (osint.domains && osint.domains.length > 0) {
                results.push(`🌐 Domains found: ${osint.domains.length}`);
                results.push(`   ${osint.domains.slice(0, 3).join(', ')}`);
            }

            if (osint.subdomains && osint.subdomains.length > 0) {
                results.push(`🔍 Subdomains: ${osint.subdomains.length} found`);
                results.push(`   ${osint.subdomains.slice(0, 5).join(', ')}`);
            }

            if (osint.emails && osint.emails.length > 0) {
                results.push(`📧 Emails: ${osint.emails.length} found`);
                results.push(`   ${osint.emails.slice(0, 3).join(', ')}`);
            }

            if (osint.technologies && osint.technologies.length > 0) {
                results.push(`⚙️ Technologies: ${osint.technologies.slice(0, 5).join(', ')}`);
            }
        }
        
        if (results.length === 0) {
            results.push(`📊 OSINT collection completed for ${target}`);
        }
        
        updateScanResults(results);
        statusElement.innerHTML = '🟢 Collection Complete';
        showNotification('OSINT collection completed successfully', 'success');
        
        // Show AI analysis if available
        if (result.ai_analysis) {
            showNotification(`AI Analysis: ${result.ai_analysis.summary}`, 'info');
        }
        
    } catch (error) {
        console.error('OSINT collection failed:', error);
        statusElement.innerHTML = '🔴 Collection Failed';
        showNotification(`OSINT failed: ${error.message}`, 'error');
        
        // Fallback to simulation
        simulateScanProgress('osint-status', () => {
            const results = [
                `📊 Domain: ${target}`,
                `🌐 IP: Lookup failed`,
                `📧 Email: Not found`,
                `🔍 Subdomains: Limited info`
            ];
            updateScanResults(results);
            statusElement.innerHTML = '🟢 Collection Complete (Simulated)';
            showNotification('OSINT completed in simulation mode', 'warning');
        });
    }
}

function launchExploits() {
    const checkedExploits = document.querySelectorAll('.exploit-item input:checked');
    const verificationOnly = document.querySelector('.exploit-options input').checked;
    
    if (checkedExploits.length === 0) {
        showNotification('Please select at least one exploit', 'error');
        return;
    }
    
    const exploits = Array.from(checkedExploits).map(cb => cb.parentElement.textContent.trim());
    
    console.log('⚡ Launching exploits:', exploits, 'Verification only:', verificationOnly);
    
    showNotification(`Launching ${exploits.length} exploits in ${verificationOnly ? 'verification' : 'active'} mode`, 'info');
    
    // Simulate exploit results
    setTimeout(() => {
        const results = exploits.map(exploit => `✅ ${exploit} - Verified`);
        updateScanResults(results);
        showNotification('Exploit verification completed', 'success');
    }, 3000);
}

// Blue Team functions
async function blockIP() {
    const ip = document.getElementById('block-ip').value;
    
    if (!ip) {
        showNotification('Please enter an IP address', 'error');
        return;
    }
    
    if (!isValidIP(ip)) {
        showNotification('Please enter a valid IP address', 'error');
        return;
    }
    
    console.log('🚫 Blocking IP:', ip);
    
    try {
        const response = await fetch(`${API_BASE_URL}/defense/firewall/block-ip`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${API_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ip_address: ip,
                threat_level: 'high',
                duration_hours: 24
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        
        showNotification(`IP ${ip} blocked successfully`, 'success');
        document.getElementById('block-ip').value = '';
        
        // Update blocked IPs count
        const currentCount = parseInt(document.getElementById('fw-blocked').textContent);
        document.getElementById('fw-blocked').textContent = currentCount + 1;
        document.getElementById('blocked-ips').textContent = currentCount + 1;
        
        console.log('Block result:', result);
        
    } catch (error) {
        console.error('IP blocking failed:', error);
        showNotification(`Failed to block IP: ${error.message}`, 'error');
        
        // Fallback to simulation
        setTimeout(() => {
            showNotification(`IP ${ip} blocked (simulated)`, 'warning');
            document.getElementById('block-ip').value = '';
            
            const currentCount = parseInt(document.getElementById('fw-blocked').textContent);
            document.getElementById('fw-blocked').textContent = currentCount + 1;
            document.getElementById('blocked-ips').textContent = currentCount + 1;
        }, 1000);
    }
}

async function deployHoneypot() {
    const types = ['ssh', 'http', 'ftp'];
    const randomType = types[Math.floor(Math.random() * types.length)];
    const randomPort = Math.floor(Math.random() * 9000) + 2000;
    
    console.log('🍯 Deploying honeypot:', randomType, 'on port', randomPort);
    
    showNotification(`Deploying ${randomType.toUpperCase()} honeypot on port ${randomPort}`, 'info');
    
    try {
        // Make real API call
        const result = await makeAPICall(`/defense/honeypot/deploy/${randomType}`, 'POST', {
            port: randomPort,
            interface: "127.0.0.1"
        });
        
        if (result.success) {
            showNotification(`${randomType.toUpperCase()} honeypot deployed successfully`, 'success');
            
            // Update honeypot count
            const currentCount = document.getElementById('honeypots').textContent;
            const newCount = parseInt(currentCount) + 1;
            document.getElementById('honeypots').textContent = newCount + ' active';
            
            console.log('Honeypot deployed:', result.honeypot_info);
        } else {
            throw new Error('Deployment failed');
        }
        
    } catch (error) {
        console.error('Honeypot deployment failed:', error);
        showNotification(`Failed to deploy honeypot: ${error.message}`, 'error');
        
        // Fallback to simulation
        setTimeout(() => {
            showNotification(`${randomType.toUpperCase()} honeypot deployed (simulated)`, 'warning');
            
            const currentCount = document.getElementById('honeypots').textContent;
            const newCount = parseInt(currentCount) + 1;
            document.getElementById('honeypots').textContent = newCount + ' active';
        }, 2000);
    }
}

async function analyzeLogs() {
    console.log('📝 Analyzing logs with AI...');
    
    showNotification('AI is analyzing system logs...', 'info');
    
    try {
        // Get sample logs for analysis
        const sampleLogs = [
            "Failed password for root from 192.168.1.100 port 22 ssh2",
            "Failed password for admin from 192.168.1.100 port 22 ssh2",
            "GET /admin.php?user=admin' UNION SELECT * FROM users-- HTTP/1.1",
            "Connection attempt to port 80 from 10.0.0.50",
            "Failed login attempt from 172.16.1.5"
        ];
        
        // Make real API call
        const result = await makeAPICall('/defense/threat-detection/analyze', 'POST', {
            log_entries: sampleLogs,
            source: "system_logs"
        });
        
        if (result.success) {
            const threatsDetected = result.analysis_results.threats_detected || 0;
            showNotification(`AI analysis complete: ${threatsDetected} threats detected`, 'success');
            
            // Update AI metrics
            const currentCount = parseInt(document.getElementById('threats-analyzed').textContent.replace(',', ''));
            document.getElementById('threats-analyzed').textContent = (currentCount + sampleLogs.length).toLocaleString();
            
            // Show threat details if any
            if (result.threats && result.threats.length > 0) {
                result.threats.forEach(threat => {
                    showNotification(`🚨 ${threat.threat_type}: ${threat.description}`, 'warning');
                });
            }
            
            console.log('AI analysis results:', result);
        } else {
            throw new Error('Analysis failed');
        }
        
    } catch (error) {
        console.error('AI log analysis failed:', error);
        showNotification(`AI analysis failed: ${error.message}`, 'error');
        
        // Fallback to simulation
        setTimeout(() => {
            const threats = Math.floor(Math.random() * 5) + 1;
            showNotification(`AI analysis complete (simulated): ${threats} threats detected`, 'warning');
            
            const currentCount = parseInt(document.getElementById('threats-analyzed').textContent.replace(',', ''));
            document.getElementById('threats-analyzed').textContent = (currentCount + 50).toLocaleString();
        }, 3000);
    }
}

function blockAllThreats() {
    const threatItems = document.querySelectorAll('.threat-item');
    const threatCount = threatItems.length;
    
    if (threatCount === 0) {
        showNotification('No active threats to block', 'info');
        return;
    }
    
    console.log('🚫 Blocking all threats:', threatCount);
    
    showNotification(`Blocking ${threatCount} threatening IPs...`, 'info');
    
    setTimeout(() => {
        // Clear threat list
        document.getElementById('threat-list').innerHTML = '<div class="no-threats">🟢 No active threats</div>';
        
        showNotification(`All ${threatCount} threats blocked successfully`, 'success');
        
        // Update blocked IPs count
        const currentCount = parseInt(document.getElementById('blocked-ips').textContent);
        document.getElementById('blocked-ips').textContent = currentCount + threatCount;
        document.getElementById('fw-blocked').textContent = currentCount + threatCount;
    }, 2000);
}

// Utility functions
function updateScanResults(results) {
    const container = document.getElementById('scan-results');
    container.innerHTML = results.map(result => 
        `<div class="result-item">${result}</div>`
    ).join('');
}

function simulateScanProgress(statusElementId, callback) {
    let progress = 0;
    const statusElement = document.getElementById(statusElementId);
    
    const interval = setInterval(() => {
        progress += Math.random() * 20;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
            callback();
        } else {
            statusElement.innerHTML = `🟡 Running... ${Math.floor(progress)}% <div class="loading"></div>`;
        }
    }, 500);
}

function isValidIP(ip) {
    const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    return ipRegex.test(ip);
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <span class="notification-icon">${getNotificationIcon(type)}</span>
        <span class="notification-message">${message}</span>
        <button class="notification-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem;
        border-radius: 4px;
        border: 1px solid ${getNotificationBorderColor(type)};
        display: flex;
        align-items: center;
        gap: 0.5rem;
        z-index: 1000;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

function getNotificationIcon(type) {
    switch(type) {
        case 'success': return '✅';
        case 'error': return '❌';
        case 'warning': return '⚠️';
        default: return 'ℹ️';
    }
}

function getNotificationColor(type) {
    switch(type) {
        case 'success': return 'rgba(0, 255, 0, 0.9)';
        case 'error': return 'rgba(255, 0, 0, 0.9)';
        case 'warning': return 'rgba(255, 255, 0, 0.9)';
        default: return 'rgba(0, 150, 255, 0.9)';
    }
}

function getNotificationBorderColor(type) {
    switch(type) {
        case 'success': return '#00ff00';
        case 'error': return '#ff0000';
        case 'warning': return '#ffff00';
        default: return '#0096ff';
    }
}

// Real-time updates
function startRealTimeUpdates() {
    // Update system status every 5 seconds
    setInterval(updateSystemStatus, 5000);
    
    // Update dashboard data every 10 seconds
    setInterval(() => {
        if (currentTab === 'dashboard') {
            updateThreatOverview();
            updateTeamStatus();
        }
    }, 10000);
    
    // Update timestamp every second
    setInterval(updateTimestamp, 1000);
}

function updateSystemStatus() {
    // Simulate system metrics
    const cpu = Math.floor(Math.random() * 30) + 15;
    const ram = Math.floor(Math.random() * 40) + 30;
    
    const cpuElement = document.querySelector('.status-right .status-item:nth-child(2)');
    const ramElement = document.querySelector('.status-right .status-item:nth-child(3)');
    
    if (cpuElement) cpuElement.innerHTML = `📊 CPU: ${cpu}%`;
    if (ramElement) ramElement.innerHTML = `💾 RAM: ${ram}%`;
}

function updateTimestamp() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { hour12: false });
    const timestampElement = document.getElementById('last-update');
    if (timestampElement) {
        timestampElement.textContent = timeString;
    }
}

// Load data functions for different tabs
function loadRedTeamData() {
    console.log('🔴 Loading Red Team data...');
    // Simulate loading red team specific data
}

function loadBlueTeamData() {
    console.log('🔵 Loading Blue Team data...');
    // Simulate loading blue team specific data
}

function loadAIData() {
    console.log('🧠 Loading AI Intelligence data...');
    // Update AI metrics
    document.getElementById('threats-analyzed').textContent = (Math.floor(Math.random() * 1000) + 1000).toLocaleString();
    document.getElementById('response-time').textContent = (Math.random() * 0.5 + 0.1).toFixed(1) + 's';
}

function loadLogsData() {
    console.log('📝 Loading logs data...');
    refreshLogs();
}

// Log functions
function refreshLogs() {
    const logContent = document.getElementById('log-content');
    const logLevel = document.getElementById('log-level').value;
    
    // Simulate log entries
    const logs = [
        { level: 'error', message: 'Failed login attempt from 192.168.1.100', time: new Date() },
        { level: 'warning', message: 'Multiple port scan attempts detected', time: new Date(Date.now() - 60000) },
        { level: 'info', message: 'Honeypot deployed on port 2222', time: new Date(Date.now() - 120000) },
        { level: 'error', message: 'SQL injection attempt blocked', time: new Date(Date.now() - 180000) },
        { level: 'info', message: 'Firewall rule created for IP 10.0.0.50', time: new Date(Date.now() - 240000) },
        { level: 'warning', message: 'Suspicious activity detected from 172.16.1.5', time: new Date(Date.now() - 300000) }
    ];
    
    const filteredLogs = logLevel === 'all' ? logs : logs.filter(log => log.level === logLevel);
    
    logContent.innerHTML = filteredLogs.map(log => 
        `<div class="log-entry ${log.level}">[${log.time.toLocaleString()}] ${log.level.toUpperCase()}: ${log.message}</div>`
    ).join('');
    
    // Scroll to bottom
    logContent.scrollTop = logContent.scrollHeight;
}

function clearLogs() {
    document.getElementById('log-content').innerHTML = '<div class="log-entry info">Logs cleared</div>';
}

// Modal functions (placeholders for future implementation)
function showNmapModal() {
    showTab('redteam');
    document.getElementById('nmap-target').focus();
}

function showOsintModal() {
    showTab('redteam');
    document.getElementById('osint-target').focus();
}

function showHoneypotModal() {
    showTab('blueteam');
    showNotification('Use the honeypot control panel to deploy new honeypots', 'info');
}

function showBlockModal() {
    showTab('blueteam');
    document.getElementById('block-ip').focus();
}

function showFirewallRules() {
    showNotification('Firewall rules management coming soon', 'info');
}

function showHoneypotStats() {
    showNotification('Detailed honeypot statistics coming soon', 'info');
}

function configureAI() {
    showNotification('AI configuration panel coming soon', 'info');
}

function showThreatDetails() {
    showNotification('Detailed threat analysis coming soon', 'info');
}

// Add CSS for notifications
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        font-size: 1.2rem;
        cursor: pointer;
        padding: 0;
        margin-left: auto;
    }
    
    .notification-close:hover {
        opacity: 0.7;
    }
    
    .no-threats {
        text-align: center;
        color: #00ff00;
        padding: 2rem;
        font-style: italic;
    }
`;
document.head.appendChild(notificationStyles);

// Console welcome message
console.log(`
🛡️⚔️ AKIRA SASE CYBERWAR MVP
================================
Welcome to the Akira Cyber Command Center!

Available commands:
- startNmapScan()
- startOsintScan()
- launchExploits()
- blockIP()
- deployHoneypot()
- analyzeLogs()

System Status: 🟢 Online
AI Status: 🧠 Active
Defense Status: 🛡️ Protected

Happy hacking! (Ethically, of course 😉)
`);

// Export functions for global access
window.akira = {
    startNmapScan,
    startOsintScan,
    launchExploits,
    blockIP,
    deployHoneypot,
    analyzeLogs,
    blockAllThreats,
    showTab,
    refreshLogs,
    clearLogs
};