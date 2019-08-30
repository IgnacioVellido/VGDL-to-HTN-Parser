###############################################################################
# vgdlTypes.py
# Ignacio Vellido Expósito
# 23/08/2019
# 
# Multiple classes for the VGDL structure
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
        stype        Type of sprite
        father      Father of the sprite (can be None)
        parameters  List of optionals parameters (format: option=value)
    """
    def __init__(self, name, stype, father, parameters):
        self.name = name
        self.stype = stype
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
