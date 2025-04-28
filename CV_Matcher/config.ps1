$scriptPath = $PSScriptRoot
$configFolder = Join-Path -Path $scriptPath -ChildPath "model_config"

if (-not (Test-Path -Path $configFolder)) {
    New-Item -Path $configFolder -ItemType Directory | Out-Null
}

# ----------------------------------------------------------
# Pull the base model required for FROM
# ----------------------------------------------------------
Write-Host "Pulling base model deepseek-r1:1.5b..." -ForegroundColor Cyan
ollama pull deepseek-r1:1.5b

# ----------------------------------------------------------
# Try to remove old model if it exists
# ----------------------------------------------------------
Write-Host "Trying to remove old model deepseek-r1:1.5b_vram (if exists)..." -ForegroundColor Cyan
try {
    ollama rm deepseek-r1:1.5b_vram
} catch {
    Write-Host "Model deepseek-r1:1.5b_vram not found or already removed, continuing..." -ForegroundColor Yellow
}

# ----------------------------------------------------------
# Create the modelfile content
# ----------------------------------------------------------
$modelfile_1_5b = @"
FROM deepseek-r1:1.5b
PARAMETER num_gpu 64
PARAMETER num_ctx 6500
"@

$modelFilePath_1_5b = Join-Path -Path $configFolder -ChildPath "deepseek_1.5b_vram.modelfile"
$modelfile_1_5b | Out-File -FilePath $modelFilePath_1_5b -Encoding utf8 -NoNewline

# ----------------------------------------------------------
# Create the new model
# ----------------------------------------------------------
Write-Host "Creating 1.5b VRAM-optimized model from: $(Resolve-Path $modelFilePath_1_5b)" -ForegroundColor Cyan
ollama create deepseek-r1:1.5b_vram -f $modelFilePath_1_5b

