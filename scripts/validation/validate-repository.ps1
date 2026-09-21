$ErrorActionPreference = 'Stop'
$root = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$required = @(
    'README.md', 'docs\architecture.md', 'docs\lab-scope.md',
    'docs\investigation-methodology.md', 'docs\threat-model.md',
    'labs\05-windows-endpoint-monitoring\README.md',
    'labs\06-threat-hunting\README.md', 'labs\07-detection-engineering\README.md',
    'reports\case-001-authentication-baseline\README.md',
    'reports\case-002-platform-verification\README.md',
    'reports\case-003-controlled-detection-test\README.md',
    'scripts\collection\collect-wazuh-evidence.ps1'
)
$missing = $required | Where-Object { -not (Test-Path (Join-Path $root $_)) }
if ($missing) { throw "Missing required project files: $($missing -join ', ')" }
if (-not (Test-Path (Join-Path $root '.gitignore'))) { throw 'Missing .gitignore; evidence must not be committed.' }
if (-not (Select-String -Path (Join-Path $root '.gitignore') -Pattern '^evidence/$' -Quiet)) { throw '.gitignore must exclude evidence/.' }
Write-Host "PASS: evidence-first project structure is complete at $root"
