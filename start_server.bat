@echo off
cd /d "C:\Users\deepe\OneDrive\Desktop\tom"
C:\Users\deepe\AppData\Local\Programs\Python\Python311\Scripts\uvicorn.exe tom_api:app --reload
pause
