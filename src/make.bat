
@ECHO OFF

set option=%1
set vgdl-file=%2
set output=%3

IF NOT x%option:build=% == x%option% (
  ECHO Compiling the grammar...
  >nul 2>nul cmd /c antlr4 -Dlanguage=Python3 Vgdl.g4
  ECHO Done
) 

IF NOT x%option:run=% == x%option% (  
  IF "%vgdl-file%" == "" (
    ECHO Wrong number of arguments
    ECHO Usage: make.bat run [VGDL file]
  ) ELSE (
    ECHO ------- Parsed tree -----------
    python Main.py %vgdl-file% %output%
  )
) 

IF NOT x%option:test1=% == x%option% (  
  test\htnp\htnp.exe -d domain.pddl -p test\problem.pddl
) 

IF NOT x%option:test2=% == x%option% (  
  test\htnp\htnp.exe -d domain.pddl -p problem.pddl
) 

IF NOT x%option:verbose1=% == x%option% (  
  test\htnp\htnp.exe -d domain.pddl -p test\problem.pddl -v
) 

IF NOT x%option:verbose2=% == x%option% (  
  test\htnp\htnp.exe -d domain.pddl -p problem.pddl -v
) 

IF NOT x%option:help=% == x%option% (  
  ECHO Usage ---------------------------
  ECHO To build: make.bat build 
  ECHO To run: make.bat run [VGDL file]
)

@ECHO ON