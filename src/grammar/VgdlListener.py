###############################################################################
# vgdlListener.py
# Ignacio Vellido Expósito
# 21/08/2019
# 
# ANTLR Listener. Reads tokens and stores in the corresponding data structure.
###############################################################################

from antlr4 import *
if __name__ is not None and "." in __name__:
    from .VgdlParser import VgdlParser
else:
    from VgdlParser import VgdlParser

import sys

from vgdl.typesVGDL import *
# from hpdl.typesHPDL import *

# from hpdl.avatarHPDL import *
# from hpdl.spriteHPDL import *
# from hpdl.interactionHPDL import *

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################
# Auxiliar functions

# Returns a list with each parameter in the token
def get_rule_parameters(list_par):
    parameters = []
    for p in list_par:
        parameters.append(p.getText())

    return parameters

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

# This class defines a complete listener for a parse tree produced by VgdlParser.
class VgdlListener(ParseTreeListener):
    """ 
    This class defines a complete listener for a parse tree produced by VgdlParser.

    Atributes:
        types       List of pairs string-string (class, object)
        predicates  List of strings
        functions   List of strings
        tasks       List of strings
        actions     List of strings
    """
    def __init__(self):
        # To parse the VGDL game description - from vgdlTypes.py
        self.sprites = []
        self.interactions = []
        self.terminations = []

        # For the level parser
        self.mappings    = []   # An array of LevelMapping        
        self.short_types = []   # The char part of a LevelMapping
        self.long_types  = []   # The sprites part of a LevelMapping
        self.hierarchy   = {}   # Dictionary with the parents of each long_type
        self.stypes      = set()   # All types in the game (bigger than long_types)
        self.transformTo = []   # Objects that can be created 
                                # ADD LATER THE SPAWNPOINTS TOO

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def f7(self, seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]
        
    # -------------------------------------------------------------------------
    
    def assign_short_long_types(self):
        """ From the LevelMap, stores short and the long name """
        for m in self.mappings:
            self.short_types.append(m.char)
            self.long_types.append(m.sprites)

    # -------------------------------------------------------------------------


    def assign_hierarchy(self):
        """ Stores a hierarchy of the objects """
        for obj in self.hierarchy:
            self.hierarchy[obj].append("Object")
            self.hierarchy[obj] = self.f7(self.hierarchy[obj])

        # Adding Object with no father
        self.hierarchy["Object"] = []

        # Deleting None from hierarchy
        for obj in self.hierarchy:
            if None in self.hierarchy[obj]:
                self.hierarchy[obj].remove(None)

    # -------------------------------------------------------------------------

    def assign_stypes(self):
        for key in self.hierarchy:
            self.stypes.add(key)
            self.stypes.update(self.hierarchy[key])


    ###########################################################################
    # -------------------------------------------------------------------------
    ###########################################################################

    def enterBasicGame(self, ctx:VgdlParser.BasicGameContext):
        pass

    def exitBasicGame(self, ctx:VgdlParser.BasicGameContext):
        self.assign_hierarchy()
        self.assign_short_long_types()        
        self.assign_stypes()
        # pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterSpriteSet(self, ctx:VgdlParser.SpriteSetContext):
        self.sprites = []

    def exitSpriteSet(self, ctx:VgdlParser.SpriteSetContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterRecursiveSprite(self, ctx:VgdlParser.RecursiveSpriteContext):        
        parentCtx = ctx.parentCtx
        if hasattr(parentCtx, 'name'):
            parent_name = parentCtx.name.text

            # Keeping the hierarchy on a structure (if key not defined, initialize it)
            # In this case, the father
            self.hierarchy.setdefault(ctx.name.text, []).append(parent_name)
            self.hierarchy.setdefault(ctx.name.text, []).extend(self.hierarchy[parent_name])

        # If it has a type, include it (if not, father must have one)
        if hasattr(ctx, 'spriteType') and hasattr(ctx.spriteType, 'text'):
            stype = ctx.spriteType.text
            self.hierarchy.setdefault(stype, []).append("Object")
        else:
            # stype = None
            stype = ctx.name.text + "Stype"
            self.hierarchy.setdefault(stype, []).append("Object")

        # The stype
        self.hierarchy.setdefault(ctx.name.text, []).append(stype)

        sprite = Sprite(ctx.name.text, stype, None,
                get_rule_parameters(ctx.parameter()))

        self.sprites.append(sprite)

    def exitRecursiveSprite(self, ctx:VgdlParser.RecursiveSpriteContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterNonRecursiveSprite(self, ctx:VgdlParser.NonRecursiveSpriteContext):
        # If it has parent, include it
        parentCtx = ctx.parentCtx        

        if hasattr(parentCtx, 'name'):
            parent_name = parentCtx.name.text

            # The father and his hierarchy
            self.hierarchy.setdefault(ctx.name.text, []).append(parent_name)
            self.hierarchy.setdefault(ctx.name.text, []).extend(self.hierarchy[parent_name])
        else:
            parent_name = None

        # If it has a type, include it (if not, father must have one)
        if hasattr(ctx, 'spriteType') and hasattr(ctx.spriteType, 'text'):
            stype = ctx.spriteType.text

            # The stype
            self.hierarchy.setdefault(ctx.name.text, []).append(stype)
            self.hierarchy.setdefault(stype, []).append("Object")
        else:
            stype = parent_name

        sprite = Sprite(ctx.name.text, stype, parent_name,
                        get_rule_parameters(ctx.parameter()))

        # Check if avatar
        if sprite.stype is not None and "avatar" in sprite.stype.lower():
            self.avatar = sprite

        self.sprites.append(sprite)        
    

    def exitNonRecursiveSprite(self, ctx:VgdlParser.NonRecursiveSpriteContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterLevelMapping(self, ctx:VgdlParser.LevelMappingContext):
        for level in ctx.LEVELDEFINITION():            
            char, sprites = level.getText().split(">", 1)

            # We only want the single character in char, no spaces 
            char = char.strip()

            # There can't be two stypes defined, only one
            sprites = sprites.split()            
            sprites = sprites[-1].strip()   # Getting the last one defined

            l = LevelMap(char, sprites)
            self.mappings.append(l)

    def exitLevelMapping(self, ctx:VgdlParser.LevelMappingContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterInteractionSet(self, ctx:VgdlParser.InteractionSetContext):
        self.interactions = []

    def exitInteractionSet(self, ctx:VgdlParser.InteractionSetContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterInteraction(self, ctx:VgdlParser.InteractionContext):
        for sprite2 in ctx.WORD()[1::]:
            if sprite2.getText() != ctx.interactionType.text:
                interaction = Interaction(ctx.sprite1.text, sprite2.getText(),
                                ctx.interactionType.text, 
                                get_rule_parameters(ctx.parameter()))

                self.interactions.append(interaction)

                # Check if an object can be produced with the interaction                                
                if "transformto" in interaction.type.lower():
                    for par in interaction.parameters:                        
                        if "stype" in par:
                            item = par.split('=')[1]
                            # Check for duplicates
                            if item not in self.transformTo:
                                self.transformTo.append(item)

    def exitInteraction(self, ctx:VgdlParser.InteractionContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterTerminationSet(self, ctx:VgdlParser.TerminationSetContext):
        self.terminations = []

    def exitTerminationSet(self, ctx:VgdlParser.TerminationSetContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterTerminationCriteria(self, ctx:VgdlParser.TerminationCriteriaContext):        
        if ctx.TRUE():
            win = True
        else:
            win = False        

        termination = Termination(ctx.WORD().getText(), win, 
                                        get_rule_parameters(ctx.parameter()))
        self.terminations.append(termination)

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