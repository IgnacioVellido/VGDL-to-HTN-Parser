/*
  Vgdl.g4
  Grammar definition for a VGDL file following ANTLR4 syntaxis

  Ignacio Vellido Expósito
  09/08/2019

  Only works in Java
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
                   | DEDENT | INDENT | NL )* DEDENT 
  ;


// SpriteSet ------------------------------------------------------------------
spriteSet
  : 'SpriteSet' INDENT (NL* spriteDefinition NL*)+ DEDENT 
  ;

spriteDefinition
  : name=WORD WS* '>' WS* spriteType=WORD? parameter* INDENT (WS* spriteDefinition NL?)+ DEDENT # RecursiveSprite
  | name=WORD WS* '>' WS* spriteType=WORD? parameter*   # NonRecursiveSprite
  // If second WORD is not defined, is a child
  ;


// LevelMapping ---------------------------------------------------------------
levelMapping
  : 'LevelMapping' INDENT (NL* LEVELDEFINITION NL*)+ DEDENT 
  ;  


// InteractionSet -------------------------------------------------------------
interactionSet
  : 'InteractionSet' INDENT (NL* interaction NL*)+ DEDENT 
  ;

interaction
  : sprite1=WORD list_sprite2=WORD+ WS* '>' interactionType=WORD parameter* 
  ;


// TerminationSet -------------------------------------------------------------
terminationSet
  : 'TerminationSet' INDENT (NL* terminationCriteria NL*)+ DEDENT
  ;

terminationCriteria
  : WORD parameter* 'win='(TRUE | FALSE) parameter* 
  ;


// Others ---------------------------------------------------------------------
parameter
  : left=WORD '=' (WORD | TRUE | FALSE ) # NonPathParameter
  | left=WORD '=' (WORD '/' WORD)  # PathParameter
  ; 

/* ----------------------------------------------------------------------------
                               Lexer rules
  -----------------------------------------------------------------------------
 */ 

COMMENT
  : '#' ~[\r\n]* -> skip ;

NL  // NewLine
  : ('\r'? '\n' ' '*) ;

WS  // WhiteSpace
  : [ \t]+ -> skip ;  // Skip spaces and tabs


// These rules are ambiguous, this order of definition must be maintained
// Maybe these two are not relevant, we should be able to know wich one is defined
// just looking at what word accompanies 'win='
TRUE
  : [Tt] [Rr] [Uu] [Ee] 
  ;
FALSE
  : [Ff] [Aa] [Ll] [Ss] [Ee] 
  ; 

WORD
  : CHAR (CHAR | UNDERSCORE | NUMBER)* 
  | NUMBER 
  ;


// Probably too big for a lexer rule, but the definition of a SYMBOL lexer
// rule generates ambiguity
LEVELDEFINITION
  : WS* SYMBOL WS* '>' WS* (WORD WS*)+ 
  ;

ANY
  : . // Ignore everything not recognised
  ;


fragment SYMBOL
  : ~[ ] ;
fragment CHAR
  :  [a-zA-Z/.] ;
fragment UNDERSCORE
  : '_' ;
fragment NUMBER
  : '-'? [0-9]+ ([.,] [0-9]+)? ;  // Can be negative or decimal
