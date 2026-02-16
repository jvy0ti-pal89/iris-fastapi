# run_server.ps1 - Stop any process on :8000, start uvicorn, and POST a test request.
$project = 'C:\Users\hp\iris-fastapi'
$port = 8000

Set-Location $project

# Stop process using port (if any)
$pid = (Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique)
if ($pid) { Stop-Process -Id $pid -Force; Write-Output "Stopped process $pid on port $port" } else { Write-Output "No process on port $port" }

# Start uvicorn in background
$proc = Start-Process -FilePath python -ArgumentList '-m','uvicorn','app.main:app','--reload','--host','127.0.0.1','--port',$port -WorkingDirectory $project -PassThru
Write-Output "Started uvicorn (PID $($proc.Id)). Waiting for startup..."
Start-Sleep -Seconds 2

# Test endpoint
try {
  $resp = Invoke-RestMethod -Uri "http://127.0.0.1:$port/predict" -Method Post -ContentType "application/json" -Body '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
  $resp | ConvertTo-Json -Depth 5
} catch {
  Write-Output "Request failed:"
  Write-Output $_.Exception.Message
}
