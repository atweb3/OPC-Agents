@echo off
setlocal
cd /d %~dp0
python -m personal_opc_workflows run-all --output opc_workflow_output
if errorlevel 1 exit /b %errorlevel%
echo.
echo 全部示例工作流已运行。请查看：%cd%\opc_workflow_output
