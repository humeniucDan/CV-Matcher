$scriptPath = $PSScriptRoot
$configFolder = Join-Path -Path $scriptPath -ChildPath "model_config"

if (-not (Test-Path -Path $configFolder)) {
    New-Item -Path $configFolder -ItemType Directory | Out-Null
}

ollama rm deepseek-r1:8b_vram
ollama rm deepseek-r1:7b_vram

# ----------------------------------------------------------
# Modelul deepseek-r1:7b_vram
# ----------------------------------------------------------
$modelfile7b = @"
FROM deepseek-r1:7b
PARAMETER num_gpu 64
PARAMETER num_ctx 2048
"@

$7bPath = Join-Path -Path $configFolder -ChildPath "deepseek_7b_vram.modelfile"
Set-Content -Path $7bPath -Value $modelfile7b

Write-Host "Creating 7B model from: $(Resolve-Path $7bPath)" -ForegroundColor Cyan
ollama create deepseek-r1:7b_vram -f $7bPath

# ----------------------------------------------------------
# Modelul deepseek-r1:8b_vram
# ----------------------------------------------------------
$modelfile8b = @"
FROM deepseek-r1:8b
PARAMETER num_gpu 128
PARAMETER num_ctx 3072
"@

$8bPath = Join-Path -Path $configFolder -ChildPath "deepseek_8b_vram.modelfile"
Set-Content -Path $8bPath -Value $modelfile8b

Write-Host "`nCreating 8B model from: $(Resolve-Path $8bPath)" -ForegroundColor Cyan
ollama create deepseek-r1:8b_vram -f $8bPath

Write-Host "`nConfig files saved in: $configFolder" -ForegroundColor Green
Write-Host "Created models:" -ForegroundColor Green
ollama list | Select-String "deepseek"

Write-Host "`nPress any key to close this window..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')