
@ECHO OFF

set arg1=%1
set arg2=%2

IF "%arg1%"=="build"  (
  antlr4 Vgdl.g4
  javac Vgdl*.java
  REM antlr4 Hello.g4  
)

IF "%arg1%"=="run" (  
  @ECHO Introduce input:
  grun Vgdl %arg2% -tree
)

IF "%arg1%"=="grun" (  
  @ECHO Introduce input:
  grun Vgdl %arg2% -gui 
)

IF "%arg1%"=="buildrun" (  
  antlr4 Vgdl.g4
  javac Vgdl*.java
  @ECHO Introduce input:
  grun Vgdl %arg2% -tree
)

IF "%arg1%"=="buildgrun" (  
  antlr4 Vgdl.g4
  javac Vgdl*.java
  @ECHO Introduce input:
  grun Vgdl %arg2% -gui
)


@ECHO ON


REM For Python: ----------------------

REM @ECHO OFF

REM set arg1=%1
REM set arg2=%2

REM IF "%arg1%"=="build"  (
REM   antlr4 -Dlanguage=Python3 Vgdl.g4
REM   REM antlr4 -Dlanguage=Python3 Hello.g4
REM )

REM IF "%arg1%"=="run" (  
REM   @ECHO Introduce input:
REM   REM py test_hello.py
REM   py test_vgdl.py
REM )

REM @ECHO ON