###############################################################################
# VgdlListener.py
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
from hpdl.typesHPDL import *

from hpdl.avatarHPDL import *
from hpdl.spriteHPDL import *
from hpdl.interactionHPDL import *

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
        self.avatar_hpdl = AvatarHPDL(self.avatar.name, 
                                      self.avatar.stype, 
                                      self.partner)

        self.assign_short_long_types()
        self.assign_hierarchy()
        self.assign_stypes()

        self.assign_types()
        self.assign_constants()
        self.assign_predicates()
        self.assign_functions()
        self.assign_tasks()
        self.assign_actions()

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

    def find_type_by_name(self, name):
        """ Find the type of a sprite given his name """
        for sprite in self.sprites:
            if sprite.name == name:
                if sprite.stype is not None:
                    return sprite.stype
                else:
                    return sprite.name
    
    def find_father_by_name(self, name):
        """ Find the type of a sprite given his name """
        for sprite in self.sprites:
            if sprite.name == name:
                if sprite.father is not None:
                    return sprite.father
                else:
                    return sprite.name

    def find_sprite_by_name(self, name):        
        for sprite in self.sprites:
            if sprite.name == name:
                return sprite

        return None

    def find_partner(self, obj):
        partner = None
        for par in obj.parameters:
            if "stype" in par:                
                partner = par.split("=")[1]
                partner = self.find_sprite_by_name(partner)

        return partner

    # FROM GITHUB 
    def invert_dict(self, d): 
        inverse = dict() 
        for key in d: 
            # Go through the list that is saved in the dict:
            for item in d[key]:
                # Check if in the inverted dict the key exists
                if item not in inverse: 
                    # If not create a new list
                    inverse[item] = [key] 
                else: 
                    inverse[item].append(key) 
        return inverse

    # FROM GITHUB, REMOVING DUPLICATES WITHOUT CHANGING ORDER
    def f7(self, seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    # -------------------------------------------------------------------------

    def assign_types(self):
        """ Object, the types of each sprite and the sprites in their hierarchy """        
        stypes = []
        names = []

        for sprite in self.sprites:
            names.append(sprite.name)

            if sprite.stype is not None:
                stypes.append(sprite.stype)
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

        """ Detectar que moving no se ha declarado (el objeto no está en types),
        buscar sus hijos directos (de aquellos hijos, los que no tengan a otro
        como padre), eliminar sus tipos de objects y añadirlos a moving, añadir
        moving a object """

        inverted_hierarchy = self.invert_dict(self.hierarchy)
    
        for obj in inverted_hierarchy:
            if obj != 'Object':
                to_add = False
                for types in self.types:
                    if obj in types:
                        to_add = True

            if not to_add:
                childs = inverted_hierarchy[obj]

                to_remove = []

                for c in childs:
                    father = self.find_father_by_name(c)

                    if father in childs:
                        to_remove.append(self.find_type_by_name(father))
                    if father == obj:
                        to_remove.append(self.find_type_by_name(c))

                to_remove = self.f7(to_remove)
                self.types.append([obj] + to_remove)

                copy_types = []
                for i in range(0, len(self.types)):
                    if self.types[i][0] == 'Object':
                        for x in to_remove:
                            try:
                                self.types[i].remove(x)
                            except ValueError:
                                pass

                    copy_types.append(self.types[i])

                self.types = copy_types            

                for i in range(0, len(self.types)): 
                    if self.types[i][0] == 'Object':
                        self.types[i].append(obj)

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
        self.predicates.append("(regenerate-interaction ?o1 ?o2 - Object)")

    # -------------------------------------------------------------------------

    def assign_functions(self):
        """ One for each coordinate; one counter for each type of object in the game 
        and one counter for each resource """
        self.functions.append("(coordinate_x ?o - Object)")
        self.functions.append("(coordinate_y ?o - Object)")
        self.functions.append("(last_coordinate_x ?o - Object)")
        self.functions.append("(last_coordinate_y ?o - Object)")

    
        for sprite in self.types:        
            # If resource, add an special counter for the avatar
            if "Resource" in sprite[0]:
                self.functions.append("(resource_" + sprite[1] + " ?a - " 
                                        + self.avatar.name + ")")

        for t in self.hierarchy:
            if t is not "":
                self.functions.append("(counter_" + t + ")")

        self.functions.append("(turn)")

    # -------------------------------------------------------------------------

    def assign_tasks(self):
        # Main task ------------------
        finish = Method("finish_game", ["(= (turn) 10)"], [])    # UNFINISHED PRECONDITION
        if self.partner is not None:
            turn   = Method("turn",
                            [],
                            ["(turn_avatar ?a - " + self.avatar.stype + " ?p - " + self.partner.name + ")",
                            "(turn_objects)",
                            "(check-interactions)",
                            "(create-interactions)",
                            "(:inline () (increase (turn) 1))",
                            "(Turn)"
                            ])
        else:
            turn   = Method("turn",
                            [],
                            ["(turn_avatar ?a - " + self.avatar.stype + ")",
                            "(turn_objects)",
                            "(check-interactions)",
                            "(create-interactions)",
                            "(:inline () (increase (turn) 1))",
                            "(Turn)"
                            ])
        # undone = Method("turn_undone", [], ["(Turn)"])  # UNFINISHED TASKS

        turn_task = Task("Turn", [], [finish, turn])
        self.tasks.append(turn_task)

        # Avatar turn ----------------        
        self.tasks.append(self.avatar_hpdl.task)

        # Rest of objects turn ------- THERE MUST BE A BETTER WAY
        object_tasks = []

        for obj in self.sprites:
            partner = self.find_partner(obj)
            methods = SpriteHPDL(obj.name, obj.stype, partner).methods

            for met in methods:
                object_tasks.extend(met.task_predicates)

        turn = Method("turn", [], object_tasks)
        task_object = Task("turn_objects", [], [turn])

        self.tasks.append(task_object)

        # Create interactions -------- 
        create_interaction_methods = []
        create_interaction_methods.append(Method("create", ["(not (evaluate-interaction ?o1 - Object ?o2 - Object))"],
                        ["(:inline () (evaluate-interaction ?o1 ?o2))"]))

        create_interaction_methods.append(Method("base_case", [], [])) # Base case
        create_interac = Task("create-interactions", [], create_interaction_methods)
        
        self.tasks.append(create_interac)

        # Check interactions --------- 
        object_interac = []
        object_methods = []
        
        for interaction in self.interactions:
            sprite_stype  = self.find_type_by_name(interaction.sprite_name)
            partner_stype = self.find_type_by_name(interaction.partner_name)
            object_methods.append(InteractionMethods(interaction.sprite_name, 
                                                     sprite_stype,
                                                     interaction.partner_name, 
                                                     partner_stype,
                                                     interaction.type,
                                                     interaction.parameters)
                                                     .get_methods())

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
        for obj in self.sprites:
            partner = self.find_partner(obj)
            actions = SpriteHPDL(obj.name, obj.stype, partner).actions

            if actions:
                self.actions.extend(actions)

        # And one for each interaction
        for interaction in self.interactions:
            sprite_stype  = self.find_type_by_name(interaction.sprite_name)
            partner_stype = self.find_type_by_name(interaction.partner_name)
            self.actions.append(InteractionActions(interaction.sprite_name, 
                                                    sprite_stype,
                                                    interaction.partner_name, 
                                                    partner_stype,
                                                    interaction.type,
                                                    interaction.parameters,
                                                    self.hierarchy)
                                                    .get_actions())
        
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
            # self.hierarchy[obj] = list(set(self.hierarchy[obj]))  # Removing duplicates

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
            stype = None

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
            self.avatar = Sprite(sprite)

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