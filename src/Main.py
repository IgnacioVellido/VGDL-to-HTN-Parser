###############################################################################
# Main.py
# Ignacio Vellido Expósito
# 20/08/2019
# 
# Parse a VGDL file into a HPDL domain, using Vgdl.g4 grammar
###############################################################################

import sys
import os.path
from antlr4 import *

from VgdlLexer import VgdlLexer
from VgdlParser import VgdlParser

from antlr4.tree.Trees import Trees

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# UNTESTED
# Receiving argument '-help' or '-h', prints Help
def GetHelp():
    help_text = """
---------------------------- antlr-vgdl -------------------------------
-----------------------------------------------------------------------
Python parser that transform a VGDL game description into a HPDL domain
Usage: make.bat run <VGDL file> [output file]

Description -----------------------------------------------------------
antlr-vgdl is a Python parser that transform files following the 
VGDL game description into a HPDL domain. 

antlr-vgdl works with files following the VGDL, VGDL 2.0 and GVGAI 
version VGDL. All properties not relevant to the construction of the 
domain are ignored.

Usage -----------------------------------------------------------------

make.bat run <VGDL file> [output file]

VGDL ------------------------------------------------------------------
VGDL is a high-level game description language developed by Tom Schaul.

The following structure is required to domainParser.py to work:
  - A initial line, wich must include "BasicGame"

  In no particular order:
  - Following a line with "SpriteSet", the definition of game sprites. 
    The format for each line is:
      sprite_name > type [parameters]

  - Following a line with "InteractionSet", the definition of . 
    The format for each line is:
      sprite_name_1 sprite_name_2  > interaction [parameters]
    
    More sprites can be included after sprite_name_2, in which case 
    the line will be broken in multiples interaction following the
    previous format, all with sprite_name_1 as first sprite.

  - Following a line with "LevelMapping", the definition of . (OPCIONAL, NO ? SERÍA PARA problemParser.py y no para este)
    The format for each line is:
      symbol_1 > sprite_name_1

    More sprites can be included after sprite_name_1

  - Following a line with "TerminationSet", the definition of . (OPCIONAL, NO ?)
    The format for each line is:
      condition [parameters] win=[True/False]

  For more information, see:
  https://github.com/schaul/py-vgdl
  https://github.com/GAIGResearch/GVGAI
  https://github.com/rubenvereecken/py-vgdl

-----------------------------------------------------------------------
-----------------------------------------------------------------------
"""

    return help_text


# -----------------------------------------------------------------------------

# UNTESTED
"""Right now it only check if contains BasicGame, SpriteSet and InteractionSet"""
# Receiving an array of lines, checks if it contains the basic structure of a
# VGDL game description file
def CheckVGDL(lines):
    basicGame = spriteSet = interactionSet = False

    for l in lines:
        if "BasicGame" in l:
            basicGame = True
        elif "SpriteSet" in l:
            spriteSet = True
        elif "InteractionSet" in l:
            interactionSet = True

    if not basicGame or not spriteSet or not interactionSet:
        return False
    else:
        return True

# -----------------------------------------------------------------------------

# UNTESTED
# Returns a string containing the domain definition
def GetDomainDefinition():
    text = """
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; HPDL domain for a VGDL game
;;; Made with antlr-vgdl
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain VGDLGame)  
  (:requirements :strips :typing)
"""

    return text

# -----------------------------------------------------------------------------

# UNTESTED
# Returns a string with the types definition
#
# @types: 2D array, in each line, first value represents the type, the rest are
# the name of the objects
def GetTypes(types):
    start_text = """
  (:types    
"""
    end_text = """
  )
"""

    text_content = "\t\t"

    for t in types:
        type_class = t[0]

        for i in range(1, len(t)):
            text_content += t[i]

        text_content += " - " + type_class + "\n\t\t"

    return start_text + text_content + end_text


# -----------------------------------------------------------------------------

# UNTESTED
# Returns a string with the functions definition
#
# @functions: list of functions, in brackets
def GetFunctions(functions):
    start_text = """
  (:functions    
"""
    end_text = """
  )
"""

    text_content = "\t\t"

    for f in functions:
        text_content += f + "\n\t\t"

    return start_text + text_content + end_text


# -----------------------------------------------------------------------------

# UNTESTED
# Returns a string with the predicates definition
#
# @predicates: list of predicates, in brackets
def GetPredicates(predicates):
    start_text = """
  (:predicates    
"""
    end_text = """
  )
"""

    text_content = "\t\t"

    for p in predicates:
        text_content += p + "\n\t\t"

    return start_text + text_content + end_text


# -----------------------------------------------------------------------------

# UNTESTED
# Returns a string with the actions definition
#
# @actions: list of actions
def GetActions(actions):
    text = ""

    for a in actions:
        text += a

    return text


# -----------------------------------------------------------------------------

# UNTESTED
# Returns a string with the predicates definition
def GetEndDomain(predicates):
    text = """
)
"""
    return text


###############################################################################
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
###############################################################################

def main(argv):
    # -------------------------------------------------------------------------
    # Checking arguments

    input_name = ""
    output_name = ""

    # If argument "-help"

    if len(argv) == 2:
        input_name = argv[2]

        if input_name == "-help" or input_name == "-h":
            print(GetHelp())
            sys.exit()

        output_name = "domain.pddl"

    elif len(argv) == 3:
        input_name = argv[1]

        # Check if file already exits
        output_name = argv[2]

        if os.path.isfile(output_name):
            print("Correct file")
        else:
            print("Wrong file")

    else:
        raise ValueError(
            'Wrong number of arguments.\nUsage:\tmake.bat run <VGDL file> [output file]\nSee "make.bat run -help" for more information.'
        )

    # -----------------------------------------------------------------------------
    # Opening input file, separating it in lines and checking VGDL structure

    input_file = open(input_name)
    input_file.close()

    lines = [line.rstrip("\n") for line in input_file]

    if not CheckVGDL(lines):
        raise ValueError(
            'Wrong format in VGDL file.\nSee "make.bat run -help" for more information.'
        )

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    input_stream = FileStream(input_name)

    lexer = VgdlLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = VgdlParser(stream)
    tree = parser.basicGame()

    # Printing parsed tree
    print(Trees.toStringTree(tree, None, parser))

    # -------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    # Initializing auxiliar variables

    # -----------------------------------------------------------------------------
    # Opening and printing HPDL domain file

    output_file = open(output_name, "w")

    """
    text_domain = GetDomainDefinition()
    text_domain += GetTypes(list_types)
    text_domain += GetFunctions(list_functions)
    text_domain += GetPredicates(list_predicates)
    text_domain += GetActions(list_actions)
    text_domain += GetEndDomain()

    output_file.write(text_domain)
    """

    # -------------------------------------------------------------------------
    # Closing output file, exiting script

    output_file.close()

    print("Conversion made without errors.")

###############################################################################
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
###############################################################################

if __name__ == '__main__':
    main(sys.argv)