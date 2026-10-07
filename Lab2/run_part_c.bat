@echo off
cd /d "%~dp0"
echo Running part (c) same-machine comparison...
python part_c_experiment.py > results\part_c_run_log.txt 2>&1
if errorlevel 1 py part_c_experiment.py > results\part_c_run_log.txt 2>&1
type results\part_c_run_log.txt
echo.
echo Done. You can close this window.
pause
