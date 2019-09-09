###############################################################################
# HpdlVgdlListener.py
# Ignacio Vellido Expósito
# 21/08/2019
# 
# ANTLR Listener. Reads tokens and store in the corresponding data structure.
# It also creates the separate parts of HPDL.
###############################################################################

import sys
from antlr4 import *

from VgdlParser import VgdlParser
from VgdlListener import VgdlListener

from hpdl.vgdlTypes import *
from hpdl.hpdlTypes import *

from hpdl.actionsGenerators import *
from hpdl.methodsGenerators import *
from hpdl.predicatesGenerators import *

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################
# Auxiliar functions

# Returns a list with each parameter in the token
def get_rule_parameters(list):
    parameters = []
    for p in list:
        parameters.append(p.getText())

    return parameters

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class HpdlVgdlListener(VgdlListener):
    """ 
    This class defines a complete listener for a parse tree produced by VgdlParser.

    Atributes:
        types       List of pairs string-string
        predicates  List of strings
        functions   List of strings
        tasks       List of strings
        actions     List of strings
    """
    def __init__(self):
        # String arrays
        self.types      = []
        self.constants  = []
        self.predicates = []
        self.functions  = []
        self.tasks      = []
        self.actions    = []

        # Only one avatar for now
        self.avatar     = None

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def process_domain(self):
        """ 
        Generates the multiple parts of a HPDL domain, to be sent to the writer
        """
        self.assign_types()
        self.assign_constants()
        self.assign_predicates()
        self.assign_functions()
        self.assign_tasks()
        self.assign_actions()

    # -------------------------------------------------------------------------

    def assign_types(self):
        """ Object, the types of each sprite and the sprites in their hierarchy """        
        self.types.append(['Orientation', ''])

        stypes = []
        names = []

        for sprite in self.sprites:
            names.append(sprite.name)

            if sprite.stype is not None:
                stypes.append(sprite.stype)

            if sprite.stype is not None:
                self.types.append([sprite.stype, sprite.name])
            elif sprite.father is not None:
                self.types.append([sprite.father, sprite.name])
                

        stypes = list(set(stypes))  # Removing duplicates
        stypes.insert(0, 'Object')  # Inserting at the beginning
        
        # Search for duplicates in sprites names and stypes
        names.extend(stypes)
        lower_names = [x.lower() for x in names]
        duplicates = set([x for x in lower_names if lower_names.count(x) > 1])

        if len(duplicates) > 0:
            print("[ERROR] Sprite name can't be the same as the sprite type (case-insensitive)")
            print("Produced by: ", duplicates)
            exit()

        self.types.append(stypes)        

    # -------------------------------------------------------------------------

    def assign_constants(self):
        """ One for each orientation """
        
        orientation = ['Orientation', "up", "down", "left", "right"]
        self.constants.append(orientation)

    # -------------------------------------------------------------------------

    def assign_predicates(self):
        """ Depends of the avatar - Probably more needed to undo operations """
        avatar = AvatarPredicatesGenerator(self.avatar.name, self.avatar.stype).get_predicates()

        self.predicates.extend(avatar)

    # -------------------------------------------------------------------------

    def assign_functions(self):
        """ One for each coordinate; one counter for each type of object in the game 
        and one counter for each resource """
        self.functions.append("(coordinate_x ?o - Object)")
        self.functions.append("(coordinate_y ?o - Object)")

        # Getting each type of object removing duplicates
        types_names = []

        for sprite in self.types:
            types_names.append(sprite[0])
            types_names.append(sprite[1])
        
            # If resource, add an special counter for the avatar
            if sprite[0] == "Resource":
                self.functions.append("(resource_" + sprite[1] + " ?a - " 
                                        + self.avatar.name + ")")

        types_names = list(set(types_names))

        """ ERROR WHEN SPRITE AND CLASS HAVE THE SAME NAME """

        for t in types_names:
            if t is not "":
                self.functions.append("(counter_" + t + ")")


    # -------------------------------------------------------------------------

    def assign_tasks(self):
        """ UNFINISHED """
        turn_method = Method("turn", [], ["(turn_avatar ?a ?o)"]) #, "(turn_objects)", "(check_interactions)"])
        turn = Task("Turn", [["a", "FlakAvatar"], ["o", "Orientation"]], [turn_method])
        self.tasks.append(turn)

        # Avatar turn ----------------
        avatar_methods = AvatarMethodsGenerator(self.avatar.name, self.avatar.stype).get_methods()

        turn_avatar = Task("turn_avatar", [["a", self.avatar.stype], ["o", "Orientation"]], 
                            avatar_methods)
        self.tasks.append(turn_avatar)
        

        # method1 = Method("test", ["(at ?t - test)", "(at ?t2 - test)"], ["(at ?c)", "(at ?c2)"])
        # method2 = Method("test2", ["(at ?t - test)", "(at ?t2 - test)"], ["(at ?c)", "(at ?c2)"])
        # test_task = Task("Test", [["test1","test2"],["test3","test4"]],
        #                     [method1, method2])
        # self.tasks.append(test_task)

    # -------------------------------------------------------------------------

    def assign_actions(self):
        """ ?? """
        # action = Action("action", [["test1","test2"],["test3","test4"]], ["(t ?t - test)", "(t1 ?t2 - test)"], ["(c ?c - test)", "(c1 ?c2 - test)"])
        # self.actions.append(action)

        # If it has USE command, search his partner (produced sprite)
        list_avatar_use = ["FlakAvatar", "AimedAvatar", "ShootAvatar"]
        if self.avatar.stype in list_avatar_use:
            matching = [s for s in self.avatar.parameters if "stype" in s]
            partner_name = matching[0].replace("stype=", "")

            # We have the sprite name, now we need the hole object
            """Probably the entire object is not needed, it must be checked later on"""
            for sprite in self.sprites:
                if sprite.name is not None and partner_name in sprite.name:
                    partner = sprite                
            
            avatar_actions = AvatarActionsGenerator(self.avatar.name, 
                                                    self.avatar.stype).get_actions(partner)
        else:                  
            avatar_actions = AvatarActionsGenerator(self.avatar.name, 
                                                    self.vatar.stype).get_actions()

        # Getting specific avatar actions
        self.actions.extend(avatar_actions)


    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterBasicGame(self, ctx:VgdlParser.BasicGameContext):
        pass

    def exitBasicGame(self, ctx:VgdlParser.BasicGameContext):        
        self.process_domain()

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterSpriteSet(self, ctx:VgdlParser.SpriteSetContext):
        self.sprites = []

    def exitSpriteSet(self, ctx:VgdlParser.SpriteSetContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterRecursiveSprite(self, ctx:VgdlParser.RecursiveSpriteContext):        
        # If it has a type, include it (if not, father must have one)
        if hasattr(ctx, 'spriteType') and hasattr(ctx.spriteType, 'text'):
            stype = ctx.spriteType.text
        else:
            stype = None

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
        else:
            parent_name = None

        # If it has a type, include it (if not, father must have one)
        if hasattr(ctx, 'spriteType') and hasattr(ctx.spriteType, 'text'):
            stype = ctx.spriteType.text
        else:
            stype = None

        sprite = Sprite(ctx.name.text, stype, parent_name,
                        get_rule_parameters(ctx.parameter()))

        # Check if avatar
        if sprite.stype is not None and "avatar" in sprite.stype.lower():
            self.avatar = Avatar(sprite)

        self.sprites.append(sprite)        
    

    def exitNonRecursiveSprite(self, ctx:VgdlParser.NonRecursiveSpriteContext):
        pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def enterLevelMapping(self, ctx:VgdlParser.LevelMappingContext):
        self.mappings = []

        for level in ctx.LEVELDEFINITION():            
            char, sprites = level.getText().split(">", 1)
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