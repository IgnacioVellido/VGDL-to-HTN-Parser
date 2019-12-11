###############################################################################
# typesVGDL.py
# Ignacio Vellido Expósito
# 23/08/2019
#
# Multiple classes defining parts of a VGDL structure
###############################################################################


class Interaction:
    """ An effect produced by the collision of two objects

        Atributes:
            sprite_name         The sprite who suffers the interaction
            partner_name        The sprite who collisioned with the main_sprite
            interaction_type    Type of interaction
            parameters          List of optionals parameters
    """

    def __init__(
        self,
        sprite_name: str,
        partner_name: str,
        interaction_type: str,
        parameters: list,
    ):
        self.sprite_name = sprite_name
        self.partner_name = partner_name
        self.type = interaction_type
        self.parameters = parameters


###############################################################################
# -----------------------------------------------------------------------------
###############################################################################


class Termination:
    """ A condition to end the game

        Atributes:
            termination_type    Type of condition
            win                 True or False, depending if the avatar wins or loses
            parameters          List of optionals parameters
    """

    def __init__(self, termination_type: str, win: bool, parameters: list):
        self.type = termination_type
        self.win = win
        self.parameters = parameters


###############################################################################
# -----------------------------------------------------------------------------
###############################################################################


class Sprite:
    """ An object in the game

        Atributes:
            name        The name of the sprite
            stype       Type of sprite
            father      Father of the sprite (can be None)
            parameters  List of optionals parameters (format: option=value)
    """

    def __init__(self, name: str, stype: str, father: "Sprite", parameters: list):
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
            sprites     A list of objects the char is associated to
    """

    def __init__(self, char: str, sprites: list):
        self.char = char
        self.sprites = sprites
