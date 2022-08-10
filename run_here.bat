@echo off
set root=C:\ProgramData\Miniconda3
call %root%\Scripts\activate.bat %root%
call conda activate FloodVolumeCalculatorApp
call cd %~dp0
start pythonw FloodVolumeCalculator.py