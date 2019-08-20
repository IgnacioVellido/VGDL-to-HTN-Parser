
@ECHO OFF

set option=%1
set rule=%2
set vgdl-file=%3

IF NOT x%option:build=% == x%option% (
  ECHO Compiling the grammar...
  >nul 2>nul cmd /c antlr4 Vgdl.g4
  >nul 2>nul cmd /c javac Vgdl*.java
  ECHO Done
  ECHO.  
) 

IF NOT x%option:tree=% == x%option% (  
  ECHO Introduce input:
  grun Vgdl %rule% %vgdl-file% -tree
) 

IF NOT x%option:gui=% == x%option% (  
  ECHO Introduce input:
  grun Vgdl %rule% %vgdl-file% -gui
)

IF NOT x%option:tokens=% == x%option% (  
  ECHO Introduce input:
  grun Vgdl %rule% %vgdl-file% -tokens
)

@ECHO ON