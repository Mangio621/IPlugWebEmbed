@echo off
REM - CALL "$(SolutionDir)scripts\prebuild-win.bat" "$(TargetExt)" "$(BINARY_NAME)" "$(Platform)" "$(TargetPath)" "$(OutDir)"
REM set FORMAT=%1
REM set NAME=%2
REM set PLATFORM=%3
REM set BUILT_BINARY=%4

REM Running the embed resource script before build
python "..\resources\web\embed-web.py" ..\resources\web