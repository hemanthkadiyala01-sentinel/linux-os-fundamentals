[CmdletBinding()]
param(
    [string]$OutputDirectory = (Join-Path $PSScriptRoot '..\..\evidence')
)

$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$output = Join-Path $OutputDirectory "wazuh-readonly-$stamp.txt"

& {
    'Collection purpose: authorized defensive verification only'
    "Collected: $(Get-Date -Format o)"
    ''
    '=== Windows Wazuh service ==='
    Get-Service -Name 'Wazuh*' -ErrorAction SilentlyContinue |
        Select-Object Name, DisplayName, Status, StartType | Format-Table -AutoSize
    ''
    '=== Ubuntu WSL service health ==='
    'wazuh-manager='; wsl.exe -d Ubuntu -- systemctl is-active wazuh-manager
    'wazuh-indexer='; wsl.exe -d Ubuntu -- systemctl is-active wazuh-indexer
    'wazuh-dashboard='; wsl.exe -d Ubuntu -- systemctl is-active wazuh-dashboard
    'filebeat='; wsl.exe -d Ubuntu -- systemctl is-active filebeat
    ''
    '=== Ubuntu authentication baseline ==='
    wsl.exe -d Ubuntu -- bash -lc 'printf "failed_password="; grep -Eic "failed password" /var/log/auth.log; printf "pam_authentication_failures="; grep -Eic "authentication failure" /var/log/auth.log; printf "accepted_password="; grep -Eic "accepted password" /var/log/auth.log; printf "sudo_events="; grep -Eic "sudo:" /var/log/auth.log'
} | Out-File -FilePath $output -Encoding utf8

(Get-Content -Raw $output) -replace '(?i)(token|key)[=:]\s*[^\s,;]+', '$1=[REDACTED]' -replace '(?i)(\d{1,3}\.){3}\d{1,3}', '[REDACTED_IP]' | Set-Content -Path $output -Encoding utf8
Write-Host "Wrote sanitized evidence to $output"
