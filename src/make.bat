
@ECHO OFF

set option=%1
set vgdl-file=%2
set output=%3

IF NOT x%option:build=% == x%option% (
  ECHO Compiling the grammar...
  >nul 2>nul cmd /c antlr4 -Dlanguage=Python3 Vgdl.g4
  ECHO Done
) 

REM Parse a game
IF NOT x%option:game=% == x%option% (    
  python Main.py -gi vgdl-examples\boulderdash.txt
) 

REM Parse a level
IF NOT x%option:level=% == x%option% (  
  python Main.py -gi vgdl-examples\boulderdash.txt -li vgdl-examples\test_level.txt
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
  python Main.py -h
)

@ECHO ON