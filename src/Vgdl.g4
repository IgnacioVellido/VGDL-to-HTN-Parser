/*
  Vgdl.g4
  Grammar definition for a VGDL file following ANTLR4 syntaxis

  Ignacio Vellido Expósito
  09/08/2019
*/

grammar Vgdl; 

/* ----------------------------------------------------------------------------
  To manage indentation, thanks to:
  https://stackoverflow.com/questions/43622514/translating-java-to-python-in-antlr4-python3-target
  
  -----------------------------------------------------------------------------
*/ 


tokens { INDENT, DEDENT }

@lexer::members {

    # A queue where extra tokens are pushed on (see the NEWLINE lexer rule).
    self.tokens = []

    # The stack that keeps track of the indentation level.
    self.indents = []

    # The amount of opened braces, brackets and parenthesis.
    self.opened = 0

    # The most recently produced token.
    self.last_token = None

def emitToken(self, t):
    super().emitToken(t)
    self.tokens.append(t)

def nextToken(self):
    if self._input.LA(1) == Token.EOF and len(self.indents) > 0:
        # Remove any trailing EOF tokens from our buffer.
        while len(self.tokens) > 0 and self.tokens[-1].type == Token.EOF:
            del self.tokens[-1]

        # First emit an extra line break that serves as the end of the statement.
        self.emitToken(self.common_token(VgdlLexer.NEWLINE, "\n"));

        # Now emit as much DEDENT tokens as needed.
        while len(self.indents) != 0:
            self.emitToken(self.create_dedent())
            del self.indents[-1]

        # Put the EOF back on the token stream.
        self.emitToken(self.common_token(Token.EOF, "<EOF>"));

    next = super().nextToken();

    if next.channel == Token.DEFAULT_CHANNEL:
        # Keep track of the last token on the default channel.
        self.last_token = next

    if len(self.tokens) == 0:
        return next
    else:
        t = self.tokens[0]
        del self.tokens[0]
        return t

def create_dedent(self):
    from VgdlParser import VgdlParser
    dedent = self.common_token(VgdlParser.DEDENT, "")
    dedent.line = self.last_token.line
    return dedent

def common_token(self, _type,  text):
    from antlr4.Token import CommonToken
    stop = self.getCharIndex() - 1
    if len(self.text) == 0:
        start = stop
    else:
        start = stop - len(self.text) + 1
    return CommonToken(self._tokenFactorySourcePair, _type, Lexer.DEFAULT_TOKEN_CHANNEL, start, stop)

## Calculates the indentation of the provided spaces, taking the
## following rules into account:
##
## "Tabs are replaced (from left to right) by one to eight spaces
##  such that the total number of characters up to and including
##  the replacement is a multiple of eight [...]"
##
##  -- https://docs.python.org/3.1/reference/lexical_analysis.html#indentation
def getIndentationCount(self, spaces):
    count = 0
    for ch in spaces:
        if ch == '\t':
            count += 8 - (count % 8)
        else:
            count += 1
    return count

def atStartOfInput(self):
    return self._interp.column == 0 and self._interp.line == 1

}

/* ----------------------------------------------------------------------------
                                Parser rules
  -----------------------------------------------------------------------------
 */ 


// Correct solution, check in parser that it recieves each part oNEWLINEy once
basicGame
  : 'BasicGame' parameter* nlindent 
        (spriteSet | levelMapping | interactionSet | terminationSet 
                   | DEDENT | nlindent | NEWLINE )* DEDENT 
  ;


// SpriteSet ------------------------------------------------------------------
spriteSet
  : 'SpriteSet' nlindent (NEWLINE* spriteDefinition NEWLINE*)+ DEDENT 
  ;

spriteDefinition
  : name=WORD WS* '>' WS* spriteType=WORD? parameter* nlindent (WS* spriteDefinition NEWLINE?)+ DEDENT # RecursiveSprite
  | name=WORD WS* '>' WS* spriteType=WORD? parameter*   # NonRecursiveSprite
  // If second WORD is not defined, is a child
  ;  


// LevelMapping ---------------------------------------------------------------
levelMapping
  : 'LevelMapping' nlindent (NEWLINE* LEVELDEFINITION NEWLINE*)+ DEDENT 
  ;  


// InteractionSet -------------------------------------------------------------
interactionSet
  : 'InteractionSet' nlindent (NEWLINE* interaction NEWLINE*)+ DEDENT 
  ;

interaction
  : sprite1=WORD list_sprite2=WORD+ WS* '>' interactionType=WORD parameter* 
  ;


// TerminationSet -------------------------------------------------------------
terminationSet
  : 'TerminationSet' nlindent (NEWLINE* terminationCriteria NEWLINE*)+ DEDENT
  ;

terminationCriteria
  : WORD parameter* 'win='(TRUE | FALSE) parameter* 
  ;


// Others ---------------------------------------------------------------------
parameter
  : left=WORD '=' (WORD | TRUE | FALSE ) # NonPathParameter
  | left=WORD '=' (WORD '/' WORD)  # PathParameter
  ; 

// For better visualization
nlindent
  : NEWLINE INDENT
  ;

/* ----------------------------------------------------------------------------
                               Lexer rules
  -----------------------------------------------------------------------------
 */ 

COMMENT
  : '#' ~[\r\n]* -> skip ;

NEWLINE
 : ( {self.atStartOfInput()}?   SPACES
   | ( '\r'? '\n' | '\r' | '\f' ) SPACES?
   )

   {
    import re
    from VgdlParser import VgdlParser
    new_line = re.sub(r"[^\r\n\f]+", "", self._interp.getText(self._input)) #.replaceAll("[^\r\n\f]+", "")
    spaces = re.sub(r"[\r\n\f]+", "", self._interp.getText(self._input)) #.replaceAll("[\r\n\f]+", "")
    next = self._input.LA(1)

    if next == VgdlParser.EOF:
        chr_next = -1
    else:
        chr_next = chr( next )

    if self.opened > 0 or chr_next == '\r' or chr_next == '\n' or chr_next == '\f' or chr_next == '#':
        self.skip()
    else:
        self.emitToken(self.common_token(self.NEWLINE, new_line))

        indent = self.getIndentationCount(spaces)
        if len(self.indents) == 0:
            previous = 0
        else:
            previous = self.indents[-1]

        if indent == previous:
            self.skip()
        elif indent > previous:
            self.indents.append(indent)
            self.emitToken(self.common_token(VgdlParser.INDENT, spaces))
        else:
            while len(self.indents) > 0 and self.indents[-1] > indent:
                self.emitToken(self.create_dedent())
                del self.indents[-1]

   };  

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

fragment SPACES
  : [ \t]+ ;
fragment SYMBOL
  : ~[ ] ;
fragment CHAR
  :  [a-zA-Z/.] ;
fragment UNDERSCORE
  : '_' ;
fragment NUMBER
  : '-'? [0-9]+ ([.,] [0-9]+)? ;  // Can be negative or decimal
