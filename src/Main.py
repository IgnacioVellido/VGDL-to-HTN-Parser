###############################################################################
# Main.py
# Ignacio Vellido Expósito
# 20/08/2019
# 
# Parses a VGDL file into a HPDL domain, using Vgdl.g4 grammar
###############################################################################

import sys
import os.path
from antlr4 import *

from VgdlLexer import VgdlLexer
from VgdlParser import VgdlParser

# Custom listener
from hpdl.HpdlVgdlListener import HpdlVgdlListener

# Needed to show parsed tree in terminal
from antlr4.tree.Trees import Trees

# HPDL domain generator
from hpdl.domainWriter import DomainWriter

# Level parser
from hpdl.levelParser import *

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
def check_VGDL(lines):
    basicGame = spriteSet = interactionSet = terminationSet = levelMapping = False    

    for l in lines:
        if "BasicGame" in l:
            basicGame = True
        elif "SpriteSet" in l:
            spriteSet = True
        elif "InteractionSet" in l:
            interactionSet = True
        elif "LevelMapping" in l:
            levelMapping = True
        elif "TerminationSet" in l:
            terminationSet = True

    if not basicGame or not spriteSet or not interactionSet \
        or not terminationSet or not levelMapping:
        return False
    else:
        return True

# -----------------------------------------------------------------------------

# Writes domain in file
def write_output(path, text):  
    try:
        with open(path, "wb") as file:
          file.write(text.encode('utf-8'))
    except Exception as e:
        print("Cannot open file " + path)
        print(str(e))

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
        input_name = argv[1]

        if input_name == "-help" or input_name == "-h":
            print(GetHelp())
            sys.exit()

        proceed = input('Proceding con output file "domain.pddl", continue?\nY/N: ')        

        if proceed == "y" or proceed == "Y":
          print('Writing in file "domain.pddl"')
        else: 
          print('Please specify output file in command\nUsage:\tmake.bat run <VGDL file> [output file]')
          sys.exit()

        output_name = "domain.pddl"

    elif len(argv) == 3:
        input_name = argv[1]

        # Check if file already exits
        output_name = argv[2]

        if os.path.isfile(output_name):
            print("Correct file")
        else:
            print("File doesn't exist")

    else:
        raise ValueError(
            'Wrong number of arguments.\nUsage:\tmake.bat run <VGDL file> [output file]\nSee "make.bat run -help" for more information.'
        )

    # -----------------------------------------------------------------------------
    # Opening input file, separating it in lines and checking VGDL structure

    input_file = open(input_name, "r")
    lines = [line.rstrip("\n") for line in input_file]
    input_file.close()

  
    if not check_VGDL(lines):
        raise ValueError(
            'Wrong structure in VGDL file.\nSee "make.bat run -help" for more information.'
        )

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Calling the ANTLR grammar

    input_stream = FileStream(input_name)

    lexer = VgdlLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = VgdlParser(stream)
    tree = parser.basicGame()

    # Printing parsed tree
    # print(Trees.toStringTree(tree, None, parser))

    listener = HpdlVgdlListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)    

    # -------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    # Getting the domain

    types = listener.types
    constants = listener.constants
    functions = listener.functions
    predicates = listener.predicates
    tasks = listener.tasks
    actions = listener.actions

    writer = DomainWriter(types, constants, functions, predicates, tasks, actions)

    text_domain = writer.get_domain()

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Opening and printing HPDL domain file

    # try:
    #     write_output(output_name, text_domain)
    # except Exception as e:
    #     print("I shouldn't be here " + str(e))

    print("Conversion made without errors.")

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Getting the level conversion from the LevelMapping
    # w -> wall    (w = short_type, wall = long_type)
    short_types = listener.short_types
    long_types = listener.long_types

    # Parsing level
    level_path = "./vgdl-examples/test_level.txt"
    # level_path = "./vgdl-examples/boulderdash_lvl1.txt"

    level = read_level(level_path)
    objects, counters, max_size, short_types = parse_level(level, short_types, long_types)
    problem = get_problem(objects, counters, short_types, long_types, max_size)

    try:
        write_output("./problem.pddl", problem)
    except Exception as e:
        print("I shouldn't be here " + str(e))

    print("Problem defined without errors.")

###############################################################################
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
###############################################################################

if __name__ == '__main__':
    main(sys.argv)