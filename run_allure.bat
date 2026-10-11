@echo off
chcp 65001 >nul
REM TestPilot 一键生成 Allure 报告
REM 依赖：Allure CLI（见 README「测试报告」小节）
setlocal

call .venv\Scripts\activate.bat
pytest --alluredir=allure-results
allure generate allure-results -o allure-report --clean

echo.
echo 报告已生成：allure-report\index.html
echo 用浏览器打开即可查看。
endlocal
