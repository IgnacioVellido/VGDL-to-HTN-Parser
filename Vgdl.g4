grammar Vgdl; 

// From https://github.com/yshavit/antlr-denter

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

/*
  VGDL grammar:
  Parse a file in VGDL notation (initially only accepts the GVGAI version)  

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

/* ----------------------------------------------------------------------------
                                Parser rules
  -----------------------------------------------------------------------------
 */ 

// file: Algo EOF ;
// BasicGame:  'BasicGame' something(optional) newline spriteset,levelmapping... ;


// SpriteSet ------------------------------------------------------------------
// SpriteSet: 'SpriteSet' something(optional) newline list-of-sprites ;
// INDENTATION IS RELEVANT
// https://stackoverflow.com/questions/6918555/antlr-how-to-parse-a-region-within-matching-brackets-with-a-lexer
spriteSet
  : 'SpriteSet' INDENT spriteDefinition+ DEDENT ; // ✓

spriteDefinition
  : WORD WS* '>' WS* WORD? parameter* INDENT (WS* spriteDefinition NL?)+ DEDENT // ✓
  | WORD WS* '>' WS* WORD parameter* ; // ✓

// LevelMapping --------------------------------------------------------------- // ✓
// LevelMapping: 'LevelMapping' something(optional) newline list-of-mappers ;
levelMapping
  : 'LevelMapping' NL* (levelDefinition NL*)+ ; // ✓

levelDefinition
  : WS* SYMBOL WS* '>' WS* WORD+ WS* ; // ✓

// InteractionSet ------------------------------------------------------------- // ✓
// InteractionSet: 'InteractionSet' something(optional) newline list-of-interactions ; 
interactionSet
  : 'InteractionSet' NL* (interaction NL*)+ ; // ✓

interaction
  : WORD WORD+ WS* '>' WORD parameter* ; // ✓

// TerminationSet ------------------------------------------------------------- // ✓
// TerminationSet: 'TerminationSet' something(optional) newline list-of-terminations ;
terminationSet
  : 'TerminationSet' NL* (terminationCriteria NL*)+ ; // ✓

terminationCriteria
  : WORD parameter* 'win='(TRUE | FALSE) parameter* ; // ✓

// Others ---------------------------------------------------------------------
parameter
  : WORD '=' (WORD | NUMBER) ; // ✓

/* ----------------------------------------------------------------------------
                               Lexer rules
  -----------------------------------------------------------------------------
 */ 


// New line
// NL
  // : '\r'? '\n' -> skip;

NL
  : ('\r'? '\n' ' '*);

// DON'T SKIP NEWLINES YET
// WhiteSpace
WS
  : [ \t]+ -> skip ;  // Skip spaces, tabs, newlines, \r (Windows)
// WS: [ \t]+ -> skip ;  // Skip spaces, tabs
// WS: ' ' -> skip ;

// SPRITE: WORD ; // Coge esto antes que WORD en todos los casos, produciendo error
// INTERACTION_TYPE: WORD ;

// Estas reglas son ambiguas !!!
TRUE
  : ('T' | 't') ('R' | 'r') ('U' | 'u') ('E' | 'e') ; // ✓
FALSE
  : ('F' | 'f') ('A' | 'a') ('L' | 'l') ('S' | 's') ('E' | 'e') ;  // ✓
// TRUE: T R U E ;
// FALSE: F A L S E ;
NUMBER
  : '-'? DIGIT+ ([.,] DIGIT+)? ;  // ✓ // Can be negative or decimal
SYMBOL  
  : ~[>\n\t\r ] ;  // Put here non valid symbols in names and level mapping
WORD
  : [a-zA-Z]+
  // | SYMBOL 
  | (TRUE | FALSE) ;

ANY: . ;  // Ignore everything not recognised

fragment CHAR:  [a-zA-Z] ;
fragment DIGIT: [0-9] ;
fragment SPACE: [ \t] ;

// For expecific words
// fragment T: [Tt] ;
// fragment R: ('R' | 'r');
// fragment U: ('U' | 'u');
// fragment E: ('E' | 'e');
// fragment F: ('F' | 'f');
// fragment A: ('A' | 'a');
// fragment L: ('L' | 'l');
// fragment S: ('S' | 's');


/*
Si queremos separar win, lo confunde con parameter
Muchas reglas son ambiguas, coge la primera definida
Terminar con salto de línea para evitar que se lie
 */