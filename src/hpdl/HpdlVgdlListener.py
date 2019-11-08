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

from hpdl.avatar import *
from hpdl.object import *
from hpdl.interaction import *

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
        self.partner    = None

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

    def process_domain(self):
        """ 
        Generates the multiple parts of a HPDL domain, to be sent to the writer
        """
        self.search_partner()

        self.avatar_hpdl = AvatarHPDL(self.avatar.name, self.avatar.stype, 
                                      self.partner)

        self.assign_types()
        self.assign_constants()
        self.assign_predicates()
        self.assign_functions()
        self.assign_tasks()
        self.assign_actions()

        self.assign_short_long_types()
        self.assign_hierarchy()
        self.assign_stypes()

    # -------------------------------------------------------------------------

    def search_partner(self):
        """ If it has USE command, search his partner (produced sprite) """
        
        list_avatar_use = ["FlakAvatar", "AimedAvatar", "ShootAvatar"]
        if self.avatar.stype in list_avatar_use:
            matching = [s for s in self.avatar.parameters if "stype" in s]
            partner_name = matching[0].replace("stype=", "")

            # We have the sprite name, now we need the hole object
            """Probably the entire object is not needed, it must be checked later on"""
            for sprite in self.sprites:
                if sprite.name is not None and partner_name in sprite.name:
                    self.partner = sprite                

    # -------------------------------------------------------------------------

    def assign_types(self):
        """ Object, the types of each sprite and the sprites in their hierarchy """        
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
        """ Don't needed right now """
        pass

    # -------------------------------------------------------------------------

    def assign_predicates(self):
        """ Depends of the avatar - Probably more needed to undo operations """
        self.predicates.append("(orientation-up ?o - Object)")
        self.predicates.append("(orientation-down ?o - Object)")
        self.predicates.append("(orientation-left ?o - Object)")
        self.predicates.append("(orientation-right ?o - Object)")

        avatar = self.avatar_hpdl.predicates
        self.predicates.extend(avatar)

        self.predicates.append("(evaluate-interaction ?o1 ?o2 - Object)")


    # -------------------------------------------------------------------------

    def assign_functions(self):
        """ One for each coordinate; one counter for each type of object in the game 
        and one counter for each resource """
        self.functions.append("(coordinate_x ?o - Object)")
        self.functions.append("(coordinate_y ?o - Object)")
        self.functions.append("(last_coordinate_x ?o - Object)")
        self.functions.append("(last_coordinate_y ?o - Object)")

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

        for t in types_names:
            if t is not "":
                self.functions.append("(counter_" + t + ")")

        self.functions.append("(turn)")


    # -------------------------------------------------------------------------

    def assign_tasks(self):
        # Main task ------------------
        finish = Method("finish_game", ["(= (turn) 3)"], [])    # UNFINISHED PRECONDITION
        turn   = Method("turn",
                        [],
                        ["(turn_avatar ?a - " + self.avatar.name + " ?p - " + self.partner.name + ")",
                         "(turn_objects)",
                         "(check-interactions)"
                         "(create-interactions)"
                         "\n(:inline () (increase (turn) 1))"
                         "(Turn)"
                        ])
        undone = Method("turn_undone", [], ["(Turn)"])  # UNFINISHED TASKS

        turn_task = Task("Turn", [], [finish, turn, undone])
        self.tasks.append(turn_task)

        # Avatar turn ----------------        
        self.tasks.append(self.avatar_hpdl.task)

        # Rest of objects turn ------- UNFINISHED
        object_tasks = []
        turn = Method("turn", [], object_tasks)
        task_object = Task("turn_objects", [], [turn])

        self.tasks.append(task_object)

        # Create interactions -------- UNFINISHED
        interaction_methods = []

        for interaction in self.interactions:
            create = Method("create", ["(not (evaluate-interaction ?o1 - Object ?o2 - Object))"],
                            ["(:inline () (evaluate-interaction ?o1 ?o2))"])

        interaction_methods.add(Method("base_case", [], [])) # Base case
        create_interac = Task("create-interactions", [], interaction_methods)
        
        self.tasks.append(create_interac)

        # Check interactions --------- UNFINISHED
        object_interac = []
        object_methods = []
        turn = Method("turn", [], object_interac)

        base = Method("base_case", [], [])
        object_methods.append(base)

        check_interac = Task("check-interactions", [], object_methods)

        self.tasks.append(check_interac)

    

    # -------------------------------------------------------------------------

    def assign_actions(self):
        """ Calls the different actions generators """

        # Getting specific avatar actions
        avatar_actions = self.avatar_hpdl.actions
        self.actions.extend(avatar_actions)

        # And one for each deterministic movable object 
        # ...

        # And one for each interaction movable object 
        # ...
    
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
            self.hierarchy[obj] = list(set(self.hierarchy[obj]))  # Removing duplicates

        # Adding Object with no father
        self.hierarchy["Object"] = []

    # -------------------------------------------------------------------------

    def assign_stypes(self):
        for key in self.hierarchy:
            self.stypes.add(key)
            self.stypes.update(self.hierarchy[key])        


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
            self.hierarchy.setdefault(stype, []).append("Object")
        else:
            stype = None

        parentCtx = ctx.parentCtx
        if hasattr(parentCtx, 'name'):
            parent_name = parentCtx.name.text

            # Keeping the hierarchy on a structure (if key not defined, initialize it)
            # In this case, the father
            self.hierarchy.setdefault(ctx.name.text, []).append(parent_name)
            self.hierarchy.setdefault(ctx.name.text, []).extend(self.hierarchy[parent_name])


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
                            self.transformTo.append(par.split('=')[1])

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