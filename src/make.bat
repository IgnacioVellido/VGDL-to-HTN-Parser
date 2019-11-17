
@ECHO OFF

set option=%1
REM set vgdl-file=%2
REM set output=%3

IF NOT x%option:build=% == x%option% (
  ECHO Compiling the grammar...
  >nul 2>nul cmd /c antlr4 -Dlanguage=Python3 Vgdl.g4
  ECHO Done
) 

REM Parse a game
IF NOT x%option:game=% == x%option% (    
  python Main.py -gi vgdl-examples\aliens.txt
) 

REM Parse a level
IF NOT x%option:level=% == x%option% (  
  python Main.py -gi vgdl-examples\aliens.txt -li vgdl-examples\test_level.txt
) 

IF NOT x%option:test=% == x%option% (  
  test\htnp\htnp.exe -d domain.pddl -p problem.pddl
)

IF NOT x%option:verbose=% == x%option% (  
  test\htnp\htnp.exe -d domain.pddl -p problem.pddl -v
) 

IF NOT x%option:help=% == x%option% (  
  python Main.py -h
)

@ECHO ON