/*
  Vgdl.g4
  Grammar definition for a VGDL file following ANTLR4 syntaxis

  Ignacio Vellido Expósito
  09/08/2019
*/

grammar Vgdl; 

/* ----------------------------------------------------------------------------
  To manage indentation I use antlr-denter.
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
  : 'LevelMapping' INDENT (NL* LEVELDEFINITION NL*)+ DEDENT ;  


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
  : WORD '=' (WORD | TRUE | FALSE ) 
  | WORD '=' (WORD '/' WORD) ;

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

WORD
  : CHAR (CHAR | UNDERSCORE | NUMBER)* 
  | NUMBER ;

// Probably too big to be a lexer rule, but the definition of a SYMBOL lexer
// rule generates ambiguity
LEVELDEFINITION
  : WS* SYMBOL WS* '>' WS* (WORD WS*)+ ;

ANY: . ;  // Ignore everything not recognised

fragment SYMBOL
  : ~[ ] ;
fragment CHAR
  :  [a-zA-Z/.] ;
fragment UNDERSCORE
  : '_' ;
fragment NUMBER
  : '-'? [0-9]+ ([.,] [0-9]+)? ;  // Can be negative or decimal