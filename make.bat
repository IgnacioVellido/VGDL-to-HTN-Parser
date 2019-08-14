
@ECHO OFF

set arg1=%1
set arg2=%2

IF "%arg1%"=="build"  (
  antlr4 Vgdl.g4
  javac Vgdl*.java  
)

IF "%arg1%"=="tree" (  
  @ECHO Introduce input:
  grun Vgdl %arg2% -tree
)

IF "%arg1%"=="gui" (  
  @ECHO Introduce input:
  grun Vgdl %arg2% -gui 
)

IF "%arg1%"=="tokens" (  
  antlr4 Vgdl.g4
  javac Vgdl*.java
  @ECHO Introduce input:
  grun Vgdl %arg2% -tokens
)

IF "%arg1%"=="buildtree" (  
  antlr4 Vgdl.g4
  javac Vgdl*.java
  @ECHO Introduce input:
  grun Vgdl %arg2% -tree
)

IF "%arg1%"=="buildgui" (  
  antlr4 Vgdl.g4
  javac Vgdl*.java
  @ECHO Introduce input:
  grun Vgdl %arg2% -gui
)

IF "%arg1%"=="buildtokens" (  
  antlr4 Vgdl.g4
  javac Vgdl*.java
  @ECHO Introduce input:
  grun Vgdl %arg2% -tokens
)

@ECHO ON