echo "Ending other instances of the Backend Calculator"
taskkill /f /im run-dev.exe
echo "Starting Backend Calculator"
start .\EnergySharing-win32-ia32\resources\app\model\run-dev\run-dev.exe
echo "Starting Frontend Application"
start .\EnergySharing-win32-ia32\EnergySharing.exe