###############################################################################
# domainGeneratorPDDL.py
# Ignacio Vellido Expósito
# 28/09/2020
#
# Generates the different parts of a PDDL domain
###############################################################################

from vgdl.typesVGDL import *
from pddl.typesPDDL import *
from pddl.avatarPDDL import AvatarPDDL
from pddl.spritePDDL import SpritePDDL
from pddl.interactionPDDL import InteractionPDDL

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################


class DomainGeneratorPDDL:
    """ Generates the different parts of a PDDL domain """

    def __init__(
        self,
        sprites: list,
        interactions: list,
        terminations: list,
        mappings: list,
        hierarchy: dict,
        avatar: "Sprite",
    ):
        self.sprites = sprites
        self.interactions = interactions
        self.mappings = mappings  # An array of LevelMapping
        self.hierarchy = hierarchy  # Dictionary with the parents of each long_type
        self.avatar = avatar

        # String arrays
        self.types = []
        self.constants = []     # Empty
        self.predicates = []
        self.functions = []     # Empty
        self.tasks = []         # Empty
        self.actions = []

        # For the level parser
        self.partner = None
        self.stepbacks = [] # List of objects involved with the avatar in a stepback interaction
        self.killIfHasLess = [] # List of objects involved with the avatar in a killIfHasLess interaction
        self.killIfOtherHasMore = [] # List of objects involved with the avatar in a killIfOtherHasMore and stepBack interaction
        self.undoAll = {}

        self.short_types = []  # The char part of a LevelMapping
        self.long_types = []  # The sprites part of a LevelMapping
        self.stypes = set()  # All types in the game (bigger than long_types)
        self.transformTo = []  # Objects that can be created
        # ADD LATER THE SPAWNPOINTS TOO - AND PRODUCERS

        self.search_partner()
        self.find_stepbacks()
        self.find_killIfHasLess()
        self.find_killIfOtherHasMore()
        self.find_undoAll()
        self.avatarPDDL = AvatarPDDL(self.avatar, self.hierarchy, self.stepbacks, 
                                        self.killIfHasLess, self.killIfOtherHasMore, 
                                        self.partner)

        # Assign spritesPDDL
        self.spritesPDDL = []
        for obj in self.sprites:
            partner = self.find_partner(obj)
            self.spritesPDDL.append(SpritePDDL(obj, self.hierarchy, self.stepbacks, self.killIfHasLess,
                                          self.undoAll, partner))

        self.assign_types()
        # self.assign_constants()
        self.assign_predicates()
        # self.assign_functions()
        self.assign_actions()

    # -------------------------------------------------------------------------

    def search_partner(self) -> "Sprite":
        """ If it has USE command, search its partner (produced sprite) """

        list_avatar_use = ["FlakAvatar", "AimedAvatar", "ShootAvatar"]
        if self.avatar.stype in list_avatar_use:
            matching = [s for s in self.avatar.parameters if "stype" in s]
            partner_name = matching[0].replace("stype=", "")

            # We have the sprite name, now we need the hole object
            """Probably the entire object is not needed, it must be checked later on"""
            for sprite in self.sprites:
                if sprite.name is not None and partner_name in sprite.name:
                    self.partner = sprite

    def find_stepbacks(self):
        """ Finds objects involved with the avatar in a stepBack/killSprite interaction """
        for i in self.interactions:
            # Check if interaction if stepback type
            if i.type == "stepBack" or i.type == "killSprite":
                # Find if avatar is involved           
                if i.sprite_name in self.hierarchy[self.avatar.name] or i.sprite_name == self.avatar.name:
                    self.stepbacks.append(i.partner_name)

        # Remove missiles
        for o in self.sprites:
            if o.stype == "Missile" and o.name in self.stepbacks:
                self.stepbacks.remove(o.name)

    def find_killIfHasLess(self):
        """ Finds objects involved with the avatar in a killIfHasLess interaction """
        for i in self.interactions:
            # Check if interaction if stepback type
            if i.type == "killIfHasLess":
                # Find if avatar is involved           
                if i.sprite_name in self.hierarchy[self.avatar.name] or i.sprite_name == self.avatar.name:
                    parameters = [p for p in i.parameters if "resource=" in p]
                    resource = parameters[0].replace("resource=",'')
                    self.killIfHasLess.append([i.partner_name, resource])

    def find_killIfOtherHasMore(self):
        """ Finds objects involved with the avatar in a killIfOtherHasMore and stepBack interaction """
        for i in self.interactions:
            # Check if interaction if stepback type
            if i.type == "killIfOtherHasMore":
                # Find if avatar is involved           
                if i.partner_name in self.hierarchy[self.avatar.name] or i.partner_name == self.avatar.name:                    
                    # Make sure same object is involved in stepBack interaction
                    # if i.sprite_name in self.stepbacks:
                    parameters = [p for p in i.parameters if "resource=" in p]
                    resource = parameters[0].replace("resource=",'')

                    parameters = [p for p in i.parameters if "limit=" in p]
                    limit = parameters[0].replace("limit=",'')

                    self.killIfOtherHasMore.append([i.sprite_name, resource, limit])

    def find_undoAll(self):
        for i in self.interactions:
            if i.type == "undoAll":
                if i.sprite_name not in self.undoAll.keys():
                    self.undoAll[i.sprite_name] = []

                self.undoAll[i.sprite_name].append(i.partner_name)

    # -------------------------------------------------------------------------
    # Auxiliary
    # -------------------------------------------------------------------------

    def find_sprite_by_name(self, name: str) -> "Sprite":
        """ Find a sprite given his name """
        for sprite in self.sprites:
            if sprite.name == name:
                return sprite

    # -------------------------------------------------------------------------

    def find_type_by_name(self, name: str) -> str:
        """ Find the type of a sprite given his name """
        for sprite in self.sprites:
            if sprite.name == name:
                if sprite.stype is not None:
                    return sprite.stype
                else:
                    return sprite.name

    # -------------------------------------------------------------------------

    def find_father_type_by_name(self, name: str) -> str:
        """ Find the type of a sprite given his name """
        for sprite in self.sprites:
            if sprite.name == name:
                if sprite.father is not None:
                    return sprite.father
                else:
                    return sprite.name

    # -------------------------------------------------------------------------

    def find_sprite_by_name(self, name: str) -> "Sprite":
        for sprite in self.sprites:
            if sprite.name == name:
                return sprite

        return None

    # -------------------------------------------------------------------------

    def find_partner(self, obj: "Sprite") -> "Sprite":
        partner = None
        for par in obj.parameters:
            if "stype" in par:
                partner = par.split("=")[1]
                partner = self.find_sprite_by_name(partner)

        return partner

    # -------------------------------------------------------------------------

    def invert_dict(self, d: dict) -> dict:
        """ Inverts the key with the values in a dictionary """
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

    # -------------------------------------------------------------------------

    def remove_duplicates(self, seq: list) -> list:
        """ Removes duplicates without changing the order """
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def assign_types(self):
        """ Object, the types of each sprite and the sprites in their hierarchy """
        stypes = []
        names = []

        # Numerics
        self.types.append(["", "num"])

        for sprite in self.sprites:
            names.append(sprite.name)
            self.stypes.add(sprite.name)

            if sprite.stype is not None:
                stypes.append(sprite.stype)
                self.types.append([sprite.stype, sprite.name])
                self.stypes.add(sprite.stype)
            elif sprite.father is not None:  # If no stype, assign the father as stype
                self.types.append([sprite.father, sprite.name])
                self.stypes.add(sprite.father)

        stypes = list(set(stypes))  # Removing duplicates
        stypes.insert(0, "Object")  # Inserting at the beginning

        # Removing duplicates in sprites names and stypes
        names.extend(stypes)
        lower_names = [x.lower() for x in names]
        duplicates = set([x for x in lower_names if lower_names.count(x) > 1])

        if len(duplicates) > 0:
            for dup in duplicates:
                stypes.remove(dup)

        self.types.append(stypes)

        """
        Detect when an sprite is not defined; find childs; remove their type 
        from objects and add them to the sprite part; add the sprite to objects
        """

        inverted_hierarchy = self.invert_dict(self.hierarchy)

        for obj in inverted_hierarchy:
            if obj != "Object":
                to_add = False
                for types in self.types:
                    if obj in types:
                        to_add = True

            if not to_add:
                childs = inverted_hierarchy[obj]

                to_remove = []

                for c in childs:
                    father = self.find_father_type_by_name(c)

                    if father in childs:
                        to_remove.append(self.find_type_by_name(father))
                    if father == obj:
                        to_remove.append(self.find_type_by_name(c))

                to_remove = self.remove_duplicates(to_remove)
                self.types.append([obj] + to_remove)

                copy_types = []
                for i in range(0, len(self.types)):
                    if self.types[i][0] == "Object":
                        for x in to_remove:
                            try:
                                self.types[i].remove(x)
                            except ValueError:
                                pass

                    copy_types.append(self.types[i])

                self.types = copy_types

                for i in range(0, len(self.types)):
                    if self.types[i][0] == "Object":
                        self.types[i].append(obj)

    # -------------------------------------------------------------------------

    def assign_constants(self):
        """ Don't needed right now """
        pass

    # -------------------------------------------------------------------------

    def assign_predicates(self):
        """ Depends of the avatar - Probably more needed to undo operations """        
        # PDDL specific
        self.predicates.extend(
            [  "; Orientation",
               "(oriented-up ?o - Object)",
               "(oriented-down ?o - Object)",
               "(oriented-left ?o - Object)",
               "(oriented-right ?o - Object)",
               "(oriented-none ?o - Object)",

               "; Game turn order",
               "(turn-avatar)",
               "(turn-sprites)",
               "(turn-interactions)",

               "; Numerics",
               "(next ?x ?y - num)",
               "(previous ?x ?y - num)",

               "; Position",
               "(at ?x ?y - num ?o - Object)",
               "(object-dead ?o - Object)",

               "; Game specific"
            ]
        )

        avatar = self.avatarPDDL.predicates
        self.predicates.extend(avatar)

        for spPDDL in self.spritesPDDL:
            sprite = spPDDL.predicates
            self.predicates.extend(sprite)

    # -------------------------------------------------------------------------

    def assign_functions(self):
        pass

    # -------------------------------------------------------------------------

    def assign_actions(self):
        """ Calls the different actions generators """

        # Getting specific avatar actions
        avatar_actions = self.avatarPDDL.actions
        self.actions.extend(avatar_actions)

        # And one for each deterministic movable object
        for obj in self.spritesPDDL:
            actions = obj.actions

            if actions:
                self.actions.extend(actions)

        # And one for each interaction
        pairs = set()
        for interaction in self.interactions:
            sprite = self.find_sprite_by_name(interaction.sprite_name)
            partner = self.find_sprite_by_name(interaction.partner_name)

            new_actions = InteractionPDDL(interaction, sprite, partner,
                                          self.hierarchy, self.avatar.name,
                                          self.stepbacks, self.killIfHasLess,
                                          self.killIfOtherHasMore,
                                          self.undoAll).actions

            if new_actions:
                self.actions.extend(new_actions)

                # Save objects involved                
                pairs.add((interaction.sprite_name, interaction.partner_name))


        # PDDL specific actions

        # Check objects involved in interactions
        end_turn_preconditions = ["(turn-interactions)"]

        # Objecst defined as a predicate
        pred_sprite = set(self.stepbacks)
        for o in self.killIfHasLess:
            pred_sprite.add(o[0])

        for o in self.killIfOtherHasMore:
            pred_sprite.add(o[0])

        for p in pairs:
            if p[0] not in pred_sprite and p[1] not in pred_sprite:
                end_turn_preconditions.append("(not (exists (?o1 - " + p[0] + " ?o2 - " + p[1] + """ ?x ?y - num) 
                                (and
                                    (not (= ?o1 ?o2))
                                    (at ?x ?y ?o1)
                                    (at ?x ?y ?o2)
                                )
                            )
                        )""")
            elif p[0] in pred_sprite:
                end_turn_preconditions.append("(not (exists (?o1 - " + p[1] + """ ?x ?y - num) 
                                (and
                                    """ + "(is-{} ?x ?y)\n".format(p[0]) +
"""                                    (at ?x ?y ?o1)
                                )
                            )
                        )""")
            else:
                end_turn_preconditions.append("(not (exists (?o1 - " + p[0] + """ ?x ?y - num) 
                                (and
                                    """ + "(is-{} ?x ?y)\n".format(p[1]) +
"""                                    (at ?x ?y ?o1)
                                )
                            )
                        )""")

        end_turn_interactions = Action(
            "END-TURN-INTERACTIONS", # Name
            [], # Parameters
            end_turn_preconditions, # Preconditions
            ["(turn-sprites)",
			"(not (turn-interactions))"], # Effects
        )
        self.actions.append(end_turn_interactions)


        # --------------------------------------------
        # Turn-sprites and end-turn-sprites actions
        # --------------------------------------------

        spPredicates = []
        for sp in self.spritesPDDL:
            spPredicates.extend(sp.predicates)

        # Get the sprites predicates (turn-...)
        turn_predicates = [p for p in spPredicates if "(turn-" in p]
        turn_predicates.append("(not (turn-sprites))")

        self.actions.append(Action(
            "TURN-SPRITES",
            [],
            ["(turn-sprites)"],
            turn_predicates
        ))

        # Get the sprites predicates (finished-turn-...)
        finished_predicates = [p for p in spPredicates if "(finished-turn-" in p]

        # Negate them and append last predicate
        negated_finished_predicates = ["(not " +  p + ")" for p in finished_predicates]
        negated_finished_predicates.append("(turn-avatar)")
        finished_predicates.append("(not (turn-interactions))")

        self.actions.append(Action(
            "END-TURN-SPRITES",
            [],
            finished_predicates,
            negated_finished_predicates
        ))


    # -------------------------------------------------------------------------
