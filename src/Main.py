###############################################################################
# Main.py
# Ignacio Vellido Expósito
# 20/08/2019
# 
# Parse a VGDL file into a HPDL domain, using Vgdl.g4 grammar
###############################################################################

import sys
import string
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

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

class LevelObject:
    def __init__(self, name, row, col, stype):
        self.name = name
        self.row  = row
        self.col  = col
        self.stype = stype

    def toStr(self):
        return self.name + "-" + str(self.row) + "," + str(self.col) + "-" + self.stype

# Parses level file
""" 
Debería:
- Abrir archivo (eso en otra función/archivo)
- Asignar a cada objeto un nombre y guardar en una estructura la posición.
(Empezar en 0,0 e ir sumando col mientras se leen caracteres, al encontrar 
retorno de carro volver a 0 y sumar fila)
- Comprobar con el lexer que tipo de objeto es cada uno, asociarlo en la 
estructura
- Escribir el problema
  - Es estático: La cabecera y el objetivo, la definición de cada apartado
  - Dinámico: La definición de tipos, los predicados del avatar, las coordenadas
  de los objetos, sus contadores y los pares "evaluate-interaction"

- Añadir el resto de objetos hasta completar el espacio (los que no están 
definidos pero se pueden utilizar más adelante)
"""
def read_level(path):  
    try:
        with open(path, "r") as file:
            return file.read()            
    except Exception as e:
        print("Cannot open file " + path)
        print(str(e))

""" Recibe el archivo y la lista de objetos posibles (su versión acortada), 
para generar un contador para cada uno de ellos. 

A LO MEJOR ES NECESARIO OTRA LISTA CON LOS TIPOS PARA AÑADIRLAS AL CONSTRUCTOR
"""
def parse_level(level, short_types, long_types):
    """ Returns a list of LevelObjects with the objects defined 
    
    short_types and long_types must have same length, defines the stype of the
    object and the char used in the level to represent it
    """
    
    lines = level.splitlines()

    row = col = 0
    objects = []

    # To keep track of each object defined and assign differents names
    # A list of the size of types with zeros
    name_counters = [0] * len(short_types)

    # To calculate the maximum number of objects in the game
    max_size = 0

    # --------------------------------------------------------------------------
    # Some characters can create problems on the domain, it is necessary
    # to change them            
    valid_char = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    valid_used_char = valid_char.copy()
    changed_char = []
    number = 1

    # Removing the used chars        
    for m in short_types:
        try:
            valid_char.remove(m)
        except Exception as e:
            pass

    for m in short_types:
        # Because there can be mora tan 26 objects on the game, we add a 
        # counter at the end of the char if needed
        if not valid_char:
            print("valid_char empty")
            valid_char = list(string.ascii_lowercase) + list(string.ascii_uppercase)
            number += 1

        if m not in valid_used_char:
            old_char = m
            m = valid_char.pop()  

            # Replacing
            changed_char.append([old_char, m])
            short_types = [m if x == old_char else x for x in short_types]

    # --------------------------------------------------------------------------

    # Creating the LevelObjects
    for line in lines:
        for char in line:
            # Not considering spaces
            if char is not ' ' or char is not '\t':                
                # Checking for wrong characters
                if char not in valid_used_char:
                    for change in changed_char:
                        if char == change[0]:
                            char = change[1]
                            changed = True

                    # If char not found
                    if not changed:
                        raise ValueError (
                            "Wrong level definition: " + char + " not defined"
                        )

                indx = short_types.index(char)
                obj = LevelObject(char + str(name_counters[indx]), row, col,
                                    long_types[indx])                
                objects.append(obj)

                name_counters[indx] += 1

                max_size += 1
                col += 1
        
        col = 0
        row += 1    

    # Completing the definition of objects
    for (lt, st, c) in zip(long_types, short_types, name_counters):
        while c < max_size:
            obj = LevelObject(st + str(c), -1, -1, lt)
            objects.append(obj)

            c += 1

    return objects, name_counters

""" Mejor que vengan agrupados por tipos ??? """
def get_problem(objects, counters, long_types):
    problem = ""

    problem += """
(define (problem VGDLProblem) (:domain VGDLGame)
    (:objects"""
    # Defining objects
    for obj in objects:
        # First writing each one separately, but a better aproach would be to get 
        # all objects of the same type written in the same line        
        # CAREFUL, SOME OBJECT HAVE 2 PARENTS - NOT CONSIDERED YET
        problem += "\n\t\t" + obj.name + " - " + obj.stype

    # Init part
    problem += """
    )

    (:init"""
    for obj in objects:
        # Writing predicates, if any
        # Que reciba por parámetro
        # Si es avatar, misil, recurso
        predicates = ""
        if "Avatar" in obj.stype:
            print("Avatar!")
            predicates += "\n\t\t(can-move-up)"

        # Writing the coordinates of the objects
        coordinates = "\n\t\t(= (coordinate_x " + obj.name + ") " + str(obj.row) + ")"
        coordinates += "\n\t\t(= (coordinate_y " + obj.name + ") " + str(obj.col) + ")"
        coordinates += "\n\t\t(= (last_coordinate_x " + obj.name + ") -1)"
        coordinates += "\n\t\t(= (last_coordinate_y " + obj.name + ") -1)"

        # Writing the evaluate-interaction predicates
        # TARDA UNA BARBARIDAD, PERO ES LÓGICO
        evaluate = ""
        for obj2 in objects:
            if obj is not obj2:
                evaluate += "\n\t\t(evaluate-interaction " + obj.name + " " + obj2.name + ")"

        problem += predicates + coordinates + evaluate + "\n"

    # Writing the counters
    # Debería ir ascendiendo por la jerarquía e ir sumando
    # Problema al tener varios tipos
    for c, name in zip(counters, long_types):
        problem += "\n\t\t" + "(= (counter_" + name + ") " + str(c) + ")"

    # Writing goal
    problem += """
    )

    (:tasks-goal
        :tasks(
            (Turn nombre-de-avatar nombre-de-partner) MEJOR QUE NO RECIBA PARÁMETRO
        )
    )
)
"""
    return problem

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

    # -----------------------------------------------------------------------------
    # Opening and printing HPDL domain file

    # try:
    #     write_output(output_name, text_domain)
    # except Exception as e:
    #     print("I shouldn't be here " + str(e))

    # -------------------------------------------------------------------------
    # Exiting script

    print("Conversion made without errors.")

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Getting the level conversion from the LevelMapping
    # w -> wall    (w = short_type, wall = long_type)
    short_types = listener.short_types
    long_types = listener.long_types

    # Parsing level
    level_path = "./vgdl-examples/boulderdash_lvl0.txt"

    level = read_level(level_path)
    objects, counters = parse_level(level, short_types, long_types)
    problem = get_problem(objects, counters, long_types)

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