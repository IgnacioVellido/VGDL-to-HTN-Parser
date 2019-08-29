###############################################################################
# HpdlVgdlListener.py
# Ignacio Vellido Expósito
# 21/08/2019
# 
# Probably a class for the avatar will be needed (to know the type and the
# additional parameter it uses)
###############################################################################

import sys
from antlr4 import *

from VgdlParser import VgdlParser
from VgdlListener import VgdlListener

from hpdl.vgdlTypes import *
from hpdl.hpdlTypes import *

from hpdl.actionsGenerators import *

# REMOVE
# GVGAI available sprites, interactions and termination conditions

# spriteStrings = [
#     "Conveyor", "Flicker", "Immovable", "OrientedFlicker", "Passive", "Resource", "Spreader",
#     "ErraticMissile", "Missile", "RandomMissile", "Walker", "WalkerJumper",
#     "ResourcePack", "Chaser", "PathChaser", "Fleeing", "RandomInertial",
#     "RandomNPC", "AlternateChaser", "RandomAltChaser","PathAltChaser", "RandomPathAltChaser",
#     "Bomber", "RandomBomber", "Portal", "SpawnPoint", "SpriteProducer", "Door",
#     "FlakAvatar", "HorizontalAvatar", "VerticalAvatar", "MovingAvatar","MissileAvatar",
#     "OrientedAvatar","ShootAvatar", "OngoingAvatar", "OngoingTurningAvatar", "BomberRandomMissile",
#     "OngoingShootAvatar", "NullAvatar", "AimedAvatar", "PlatformerAvatar", "BirdAvatar",
#     "SpaceshipAvatar", "CarAvatar", "WizardAvatar", "LanderAvatar", "ShootOnlyAvatar", "SpawnPointMultiSprite",
#     "LOSChaser"
# ]

# effectStrings = [
#     "stepBack", "turnAround", "killSprite", "killBoth", "killAll", "transformTo", "transformToSingleton", "transformIfCount",
#     "wrapAround", "changeResource", "killIfHasLess", "killIfHasMore", "cloneSprite",
#     "flipDirection", "reverseDirection", "shieldFrom", "undoAll", "spawn", "spawnIfHasMore", "spawnIfHasLess",
#     "pullWithIt", "wallStop", "collectResource", "collectResourceIfHeld", "killIfOtherHasMore", "killIfFromAbove",
#     "teleportToExit", "bounceForward", "attractGaze", "align", "subtractHealthPoints", "addHealthPoints",
#     "transformToAll", "addTimer", "killIfFrontal", "killIfNotFrontal", "spawnBehind",
#     "updateSpawnType", "removeScore", "increaseSpeedToAll", "decreaseSpeedToAll", "setSpeedForAll", "transformToRandomChild",
#     "addHealthPointsToMax", "spawnIfCounterSubTypes", "bounceDirection", "wallBounce", "killIfSlow", "killIfAlive",
#     "waterPhysics", "halfSpeed", "killIfNotUpright", "killIfFast", "wallReverse", "spawnAbove", "spawnLeft", "spawnRight", "spawnBelow"
# ]

# terminationStrings = [
#     "MultiSpriteCounter", "SpriteCounter", "SpriteCounterMore", "MultiSpriteCounterSubTypes", "Timeout", "StopCounter"
# ]


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
        self.predicates = []
        self.functions  = []
        self.tasks      = []
        self.actions    = []

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def process_domain(self):
        """ 
        Generates the multiple parts of a HPDL domain, to be sent to the writer
        """
        self.assign_types()
        self.assign_predicates()
        self.assign_functions()
        self.assign_tasks()
        self.assign_actions()

    # -------------------------------------------------------------------------

    def assign_types(self):
        """ Object, the types of each sprite and the sprites in their hierarchy """        
        stypes = []

        for sprite in self.sprites:
            if sprite.stype is not None:
                stypes.append(sprite.stype)

            if sprite.stype is not None:
                self.types.append([sprite.stype, sprite.name])
            elif sprite.father is not None:
                self.types.append([sprite.father, sprite.name])
                

        stypes = list(set(stypes))  # Removing duplicates
        stypes.insert(0, 'Object')  # Inserting at the beginning
        
        self.types.append(stypes)        

    # -------------------------------------------------------------------------

    def assign_predicates(self):
        """ ?? """
        # Debería haber una clase para esto, por si acaso no lo hago aún
        # Si fuese otro tipo de avatar (por ejemplo OrientatedAvatar) tendría can-move-up y can-move-down
        mobility = ["(can-move-left ?a FlakAvatar)", "(can-move-right ?a FlakAvatar)"]

        self.predicates.extend(mobility)

    # -------------------------------------------------------------------------

    def assign_functions(self):
        """ One for each coordinate, one counter for each type of object in the game """
        self.functions.append("(coordinate_x ?o - Object)")
        self.functions.append("(coordinate_y ?o - Object)")

        # Getting each type of object removing duplicates
        types_names = []

        for sprite in self.types:
            types_names.append(sprite[0])
            types_names.append(sprite[1])
        
        types_names = list(set(types_names))

        for t in types_names:
            self.functions.append("(counter ?o - " + t + ")")

    # -------------------------------------------------------------------------

    def assign_tasks(self):
        """ ?? """
        # method_avatar = Method("move-avatar", ["(a"])
        # turn = Task("Turn", [], [method_avatar, method_objects, method_interactions])


        method1 = Method("test", ["(at ?t - test)", "(at ?t2 - test)"], ["(at ?c)", "(at ?c2)"])
        method2 = Method("test2", ["(at ?t - test)", "(at ?t2 - test)"], ["(at ?c)", "(at ?c2)"])
        test_task = Task("Test", [["test1","test2"],["test3","test4"]],
                            [method1, method2])

        self.tasks.append(test_task)

    # -------------------------------------------------------------------------

    def assign_actions(self):
        """ ?? """
        action = Action("action", [["test1","test2"],["test3","test4"]], ["(t ?t - test)", "(t1 ?t2 - test)"], ["(c ?c - test)", "(c1 ?c2 - test)"])

        # Searching the type of avatar
        for sprite in self.sprites:
            if sprite.stype is not None and "avatar" in sprite.stype.lower():
                avatar = sprite

        avatar_actions = AvatarActionsGenerator(avatar.name, avatar.stype).get_actions()
        self.actions.extend(avatar_actions)

        self.actions.append(action)

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