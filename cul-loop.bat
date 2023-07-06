@echo off

:loop
curl -d "follower" http://127.0.0.1:31112/function/mongodb-github/
timeout /t 1 >nul 2>&1
goto loop
