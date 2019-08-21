###############################################################################
# HpdlVgdlListener.py
# Ignacio Vellido Expósito
# 21/08/2019
# 
# VGDL correct structure should be checked here !!!!!!!!!
###############################################################################

import sys
from antlr4 import *

from VgdlParser import VgdlParser
from VgdlListener import VgdlListener

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class Interaction:
    """ An effect produced by the collision of two objects

    Atributes:
        main_sprite     The sprite who suffers the interaction
        second_sprite   The sprite who collisioned the main_sprite
        type            Type of interaction
        parameters      List of optionals parameters
    """
    def __init__(self, main_sprite, second_sprite, type, parameters):
        self.main_sprite = main_sprite
        self.second_sprite = second_sprite
        self.type = type
        self.parameters = parameters

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class Termination:
    """ A condition to end the game

    Atributes:
        type        Type of condition
        win         True or False, depending if the avatar wins or loses
        parameters  List of optionals parameters
    """
    def __init__(self, type, win, parameters):
        self.type = type
        self.win = win
        self.parameters = parameters
        

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class Sprite:
    """ A object in the game

    Atributes:
        name        The name of the sprite
        type        Type of sprite
        father      Father of the sprite (can be None)
        parameters  List of optionals parameters
    """
    def __init__(self, name, type, father, parameters):
        self.name = name
        self.type = type
        self.father = father
        self.parameters = parameters
        

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class LevelMap:
    """ A transformation of a level definition into a game sprite

    Atributes:
        char        The character in the level definition file
        sprites     The list of objects the char is associated to
    """
    def __init__(self, char, sprites):
        self.char = char
        self.sprites = sprites    

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

# This class defines a complete listener for a parse tree produced by VgdlParser.
class HpdlVgdlListener(VgdlListener):
    def __init__(self):
        self.text_domain = ""

        # String arrays
        self.types = []
        self.functions = []
        self.predicates = []
        self.actions = []

    # IF NOTHING CHANGES, DON'T NEEDED
    # def get_ouput(self):
    #     return self.text_domain

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    # Returns a string containing the domain definition
    def get_domain_definition(self):
        text = """
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; HPDL domain for a VGDL game
;;; Made with antlr-vgdl
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain VGDLGame)  
  (:requirements
    :typing
    :fluents
    :derived-predicates
    :negative-preconditions
    :universal-preconditions
    :disjuntive-preconditions
    :conditional-effects
    :htn-expansion

    ; For time management
    :durative-actions
    :metatags
  )
"""
        return text

    # -------------------------------------------------------------------------

    # Returns a string with closing the final brackets in the domain
    def get_end_domain(self):
        text = """
)
"""
        return text

    # -----------------------------------------------------------------------------

    # UNTESTED
    # Returns a string with the types definition
    #
    # @types: 2D array, in each line, first value represents the type, the rest are
    # the name of the objects
    def get_types(self, types):
        start_text = """
  (:types    
  """
        end_text = """
  )
  """

        text_content = "    "

        for t in types:
            type_class = t[0]

            for i in range(1, len(t)):
                text_content += t[i]

            text_content += " - " + type_class + "\n    "

        return start_text + text_content + end_text


    # -----------------------------------------------------------------------------

    # UNTESTED
    # Returns a string with the functions definition
    #
    # @functions: list of functions, in brackets
    def get_functions(self, functions):
        start_text = """
  (:functions    
  """
        end_text = """
  )
  """

        text_content = "    "

        for f in functions:
            text_content += f + "\n    "

        return start_text + text_content + end_text


    # -----------------------------------------------------------------------------

    # UNTESTED
    # Returns a string with the predicates definition
    #
    # @predicates: list of predicates, in brackets
    def get_predicates(self, predicates):
        start_text = """
  (:predicates    
  """
        end_text = """
  )
  """

        text_content = "    "

        for p in predicates:
            text_content += p + "\n    "

        return start_text + text_content + end_text


    # -----------------------------------------------------------------------------

    # UNTESTED
    # Returns a string with the actions definition
    #
    # @actions: list of actions
    def get_actions(actions):
        text = ""

        for a in actions:
            text += a

        return text

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterBasicGame(self, ctx:VgdlParser.BasicGameContext):
        self.text_domain = self.get_domain_definition()

    def exitBasicGame(self, ctx:VgdlParser.BasicGameContext):
        self.text_domain += self.get_end_domain()

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterSpriteSet(self, ctx:VgdlParser.SpriteSetContext):
        pass

    def exitSpriteSet(self, ctx:VgdlParser.SpriteSetContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterRecursiveSprite(self, ctx:VgdlParser.RecursiveSpriteContext):
        pass

    def exitRecursiveSprite(self, ctx:VgdlParser.RecursiveSpriteContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterNonRecursiveSprite(self, ctx:VgdlParser.NonRecursiveSpriteContext):
        pass

    def exitNonRecursiveSprite(self, ctx:VgdlParser.NonRecursiveSpriteContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterLevelMapping(self, ctx:VgdlParser.LevelMappingContext):
        pass

    def exitLevelMapping(self, ctx:VgdlParser.LevelMappingContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterInteractionSet(self, ctx:VgdlParser.InteractionSetContext):
        pass

    def exitInteractionSet(self, ctx:VgdlParser.InteractionSetContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    # Divide in multiple Interaction if requierd

    def enterInteraction(self, ctx:VgdlParser.InteractionContext):
        pass

    def exitInteraction(self, ctx:VgdlParser.InteractionContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterTerminationSet(self, ctx:VgdlParser.TerminationSetContext):
        pass

    def exitTerminationSet(self, ctx:VgdlParser.TerminationSetContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterTerminationCriteria(self, ctx:VgdlParser.TerminationCriteriaContext):
        pass

    def exitTerminationCriteria(self, ctx:VgdlParser.TerminationCriteriaContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterNonPathParameter(self, ctx:VgdlParser.NonPathParameterContext):
        pass

    def exitNonPathParameter(self, ctx:VgdlParser.NonPathParameterContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterPathParameter(self, ctx:VgdlParser.PathParameterContext):
        pass

    def exitPathParameter(self, ctx:VgdlParser.PathParameterContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterNlindent(self, ctx:VgdlParser.NlindentContext):
        pass

    def exitNlindent(self, ctx:VgdlParser.NlindentContext):
        pass