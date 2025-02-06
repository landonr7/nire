@echo off
setlocal enabledelayedexpansion

if not "%3"=="" (
    echo No more than three arguments, please
    goto :eof
)

set "input_directory=%~1"
set "output_directory=%~2"

:: Validate parameters
if "%input_directory%"=="" (
    echo Error: Input directory not specified
    goto :eof
)
if "%output_directory%"=="" (
    echo Error: Output directory not specified
    goto :eof
)
if not exist "%input_directory%\" (
    echo Error: Input directory "%input_directory%" does not exist
    goto :eof
)

mkdir "%output_directory%" 2>nul

for /f "delims=" %%i in ('dir /b /a-d "%input_directory%\*.txt" 2^>nul') do (
    set "input_file=%input_directory%\%%i"
    set "output_file=%output_directory%\%%~ni_out.txt"

    REM Run token.py on each file 
    python tokenizer.py "!input_file!" "!output_file!"

    REM Was file actually created?
    if exist "!output_file!" (
        echo Processed "!input_file!" to "!output_file!"
    ) else (
        echo Error: Output file "!output_file!" not created.
    )
)
:eof