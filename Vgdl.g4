/*
  antlr-vgdl:
  Parse a file in VGDL notation using ANTLR4

  Ignacio Vellido Expósito
  09/08/2019

  ✓ = Tested

  Mejoras:
  - Ahora mismo no puede haber sprites cuyo nombre sea una única letra, ya que
  se convierte en el token SYMBOL 
  - Hay reglas ambiguas
  - Si el parámetro es de GVGAI conteniendo una ruta, no funciona (no reconoce
  el caracter /)
  - Debe terminar con salto de línea
  - Para detectar la indentación necesita que no se utilice \t, sino '  ' (dos espacios)
  Quizás se puede arreglar modificando los archivos de antlr-denter
*/

grammar Vgdl; 

/* ----------------------------------------------------------------------------
  To manage indentation, I use antlr-denter.
  See https://github.com/yshavit/antlr-denter for more information
  -----------------------------------------------------------------------------
*/ 
tokens { INDENT, DEDENT }

@lexer::header {
  import com.yuvalshavit.antlr4.DenterHelper;
}

@lexer::members {
  private final DenterHelper denter = DenterHelper.builder()
    .nl(NL)
    .indent(VgdlParser.INDENT)
    .dedent(VgdlParser.DEDENT)
    .pullToken(VgdlLexer.super::nextToken);

  @Override
  public Token nextToken() {
    return denter.nextToken();
  }
}


/* ----------------------------------------------------------------------------
                                Parser rules
  -----------------------------------------------------------------------------
 */ 


// Correct solution, check in parser that it recieves each part only once
basicGame
  : 'BasicGame' parameter* INDENT 
        (spriteSet | levelMapping | interactionSet | terminationSet 
                   | DEDENT | INDENT | NL )* DEDENT ;


// SpriteSet ------------------------------------------------------------------
spriteSet
  : 'SpriteSet' INDENT (NL* spriteDefinition NL*)+ DEDENT ;

spriteDefinition
  : WORD WS* '>' WS* WORD? parameter* INDENT (WS* spriteDefinition NL?)+ DEDENT
  | WORD WS* '>' WS* WORD? parameter* ; // If second WORD is not defined, is a child


// LevelMapping ---------------------------------------------------------------
levelMapping
  : 'LevelMapping' INDENT (NL* levelDefinition NL*)+ DEDENT ;

levelDefinition
  : WS* SYMBOL WS* '>' WS* WORD+ WS* ;


// InteractionSet -------------------------------------------------------------
interactionSet
  : 'InteractionSet' INDENT (NL* interaction NL*)+ DEDENT ;

interaction
  : WORD WORD+ WS* '>' WORD parameter* ;


// TerminationSet -------------------------------------------------------------
terminationSet
  : 'TerminationSet' INDENT (NL* terminationCriteria NL*)+ DEDENT;

terminationCriteria
  : WORD parameter* 'win='(TRUE | FALSE) parameter* ;


// Others ---------------------------------------------------------------------
parameter
  : WORD '=' (WORD | NUMBER | TRUE | FALSE) 
  | WORD '=' (WORD '/' WORD)* ;


/* ----------------------------------------------------------------------------
                               Lexer rules
  -----------------------------------------------------------------------------
 */ 

NL  // NewLine
  : ('\r'? '\n' ' '*) ;

WS  // WhiteSpace
  : [ \t]+ -> skip ;  // Skip spaces and tabs


// These rules are ambiguous, this order of definition must be maintained
TRUE
  : [Tt] [Rr] [Uu] [Ee] ;
FALSE
  : [Ff] [Aa] [Ll] [Ss] [Ee] ; 
NUMBER
  : '-'? DIGIT+ ([.,] DIGIT+)? ;  // Can be negative or decimal
SYMBOL  
  : ~[>\n\t\r ] ;  // Put here non valid symbols in names and level mapping
WORD
  : [a-zA-Z]+ ;


ANY: . ;  // Ignore everything not recognised


fragment CHAR:  [a-zA-Z] ;
fragment DIGIT: [0-9] ;
fragment SPACE: [ \t] ;