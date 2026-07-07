@echo off
REM ---------------------------------------------------------------
REM  Abre o Painel de Senhas no Chrome com o som ativado
REM  (a flag --autoplay-policy desativa o bloqueio de som automatico)
REM ---------------------------------------------------------------

REM Tenta o caminho mais comum do Chrome (64 bits)
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --autoplay-policy=no-user-gesture-required --app=http://localhost:5000/painel
    goto :fim
)

REM Tenta o caminho alternativo do Chrome (32 bits)
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --autoplay-policy=no-user-gesture-required --app=http://localhost:5000/painel
    goto :fim
)

echo Nao foi possivel encontrar o Chrome nos caminhos habituais.
echo Verifica onde o Chrome esta instalado e ajusta este ficheiro.
pause

:fim