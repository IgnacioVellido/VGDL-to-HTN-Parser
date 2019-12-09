# -*- coding: utf-8 -*-
###############################################################################
# Main.py
# Ignacio Vellido Expósito
# 20/08/2019
# 
# Parses a VGDL file into a HPDL domain, using Vgdl.g4 grammar
###############################################################################

import sys
import os.path
import argparse

# For FileStream and other utilities
from antlr4 import *

from grammar.VgdlLexer import VgdlLexer
from grammar.VgdlParser import VgdlParser

# Custom listener
from grammar.VgdlListener import VgdlListener

# Needed to show parsed tree in terminal
# from antlr4.tree.Trees import Trees

# HPDL domain generator
from hpdl.domainGeneratorHPDL import DomainGeneratorHPDL
from hpdl.domainWriterHPDL import DomainWriter

# Level parser
# from hpdl.levelWriterHPDL import LevelWriter
from hpdl.levelGeneratorHPDL import *

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


# Receiving argument '-help' or '-h', prints Help
def GetHelp():
    help_text = """
Description -----------------------------------------------------------
antlr-vgdl is a Python parser that transform files following the 
VGDL game description into a HPDL domain. 

antlr-vgdl works with files following the VGDL, VGDL 2.0 and GVGAI 
version VGDL. All properties not relevant to the construction of the 
domain are ignored.

VGDL ------------------------------------------------------------------
VGDL is a high-level game description language developed by Tom Schaul.

To parse a game, the following structure is required:
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

  - Following a line with "LevelMapping", the definition of a VGDL level.
    The format for each line is:
      symbol_1 > sprite_name_1

    More sprites can be included after sprite_name_1

  - Following a line with "TerminationSet", the definition of . (OPCIONAL, NO ?)
    The format for each line is:
      condition [parameters] win=[True/False]

To parse a level, ... [TO BE COMPLETED]

  For more information, see:
  https://github.com/schaul/py-vgdl
  https://github.com/GAIGResearch/GVGAI
  https://github.com/rubenvereecken/py-vgdl

-----------------------------------------------------------------------
-----------------------------------------------------------------------
"""

    return help_text


# -----------------------------------------------------------------------------

"""Right now it only check if contains BasicGame, SpriteSet and InteractionSet"""
def check_VGDL(lines):
    """ Receiving an array of lines, checks if it contains the basic structure of a
    VGDL game description file """
    basicGame = spriteSet = interactionSet = terminationSet = levelMapping = False    

    for l in lines:
        if "basicgame" in l.lower():
            basicGame = True              
        elif "spriteset" in l.lower():
            spriteSet = True
        elif "InteractionSet" in l:
            interactionSet = True
        elif "levelmapping" in l.lower():
            levelMapping = True
        elif "terminationset" in l.lower():
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
    argparser = argparse.ArgumentParser(epilog=GetHelp(), 
                                        formatter_class=argparse.RawDescriptionHelpFormatter,
                                        description="Python parser that transform a VGDL game/level description into a HPDL domain/problem")
    argparser.add_argument("-gi", "--gameInput", required=True, 
                                help="Input VGDL game file")
    argparser.add_argument("-li","--levelInput", 
                                help="Input VGDL level file")
    argparser.add_argument("-go", "--gameOutput", default="domain.pddl", 
                                help="Ouput VGDL game file")
    argparser.add_argument("-lo","--levelOutput", default="problem.pddl", 
                                help="Ouput VGDL level file")
    argparser.add_argument("-vh","--verboseHelp", action="store_true", 
                                help="Show additional information")

    args = argparser.parse_args()

    if args.verboseHelp:
        print(GetHelp())
        sys.exit()

    # -----------------------------------------------------------------------------
    # Opening input file, separating it in lines and checking VGDL structure
    # if game is being parsed

    input_file = open(args.gameInput, "r")
    lines = [line.rstrip("\n") for line in input_file]
    input_file.close()

    if not check_VGDL(lines):
        raise ValueError(
            'Wrong structure in VGDL file.\nSee "Main.py -help" for more information.'
        )

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Calling the ANTLR grammar

    input_stream = FileStream(args.gameInput)

    lexer = VgdlLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = VgdlParser(stream)
    tree = parser.basicGame()

    listener = VgdlListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)    

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # Getting the results from the listener
    sprites = listener.sprites
    interactions = listener.interactions
    terminations = listener.terminations

    mappings = listener.mappings
    hierarchy = listener.hierarchy
    avatar = listener.avatar

    # Getting the domain
    domainGenerator = DomainGeneratorHPDL(sprites, interactions, terminations,
                                            mappings, hierarchy, avatar)
    types = domainGenerator.types
    constants = domainGenerator.constants
    functions = domainGenerator.functions
    predicates = domainGenerator.predicates
    tasks = domainGenerator.tasks
    actions = domainGenerator.actions
    
    # types = listener.types
    # constants = listener.constants
    # functions = listener.functions
    # predicates = listener.predicates
    # tasks = listener.tasks
    # actions = listener.actions

    # ----------------------------------------------------------------------

    writer = DomainWriter(types, constants, functions, predicates, tasks, actions)
    text_domain = writer.get_domain()

    # ----------------------------------------------------------------------
    # Opening and printing HPDL domain file

    try:
        write_output(args.gameOutput, text_domain)
    except Exception as e:
        print("I shouldn't be here " + str(e))


    print("Game parsed without errors.")
    # ----------------------------------------------------------------------

    if args.levelInput:
        # ----------------------------------------------------------------------
        # Getting the level conversion from the LevelMapping
        # w -> wall    (w = short_type, wall = long_type)
        short_types = listener.short_types
        long_types = listener.long_types
        hierarchy = listener.hierarchy
        stypes = listener.stypes
        transformTo = listener.transformTo
        avatarHPDL = domainGenerator.avatarHPDL

        # ----------------------------------------------------------------------
        # Parsing level
        level = read_level(args.levelInput)
        objects, max_size, short_types, counters = parse_level(level, short_types, 
                                                                long_types, transformTo)
        problem = get_problem(objects, counters, short_types, long_types, 
                                max_size, hierarchy, stypes, listener.sprites,
                                avatarHPDL)

        # ----------------------------------------------------------------------
        # Writing ouput
        try:
            write_output(args.levelOutput, problem)
        except Exception as e:
            print("I shouldn't be here " + str(e))

        print("Problem defined without errors.")

###############################################################################
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
###############################################################################

if __name__ == '__main__':
    main(sys.argv)