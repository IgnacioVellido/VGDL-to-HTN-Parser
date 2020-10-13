###############################################################################
# domainGeneratorPDDL.py
# Ignacio Vellido Expósito
# 28/09/2020
#
# Generates the different parts of a PDDL domain
###############################################################################

from vgdl.typesVGDL import *
from pddl.typesPDDL import *
from pddl.avatarPDDL import *
from pddl.spritePDDL import *
from pddl.interactionPDDL import *

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
        self.short_types = []  # The char part of a LevelMapping
        self.long_types = []  # The sprites part of a LevelMapping
        self.stypes = set()  # All types in the game (bigger than long_types)
        self.transformTo = []  # Objects that can be created
        # ADD LATER THE SPAWNPOINTS TOO

        self.search_partner()
        self.avatarPDDL = AvatarPDDL(self.avatar, self.hierarchy, self.partner)
        self.spritesPDDL = []

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
        self.predicates.extend(
            ["(oriented-up ?o - Object)",
                "(oriented-down ?o - Object)",
                "(oriented-left ?o - Object)",
                "(oriented-right ?o - Object)"]
        )

        avatar = self.avatarPDDL.predicates
        self.predicates.extend(avatar)

        for spPDDL in spritesPDDL:
            sprite = spPDDL.predicates
            self.predicates.extend(sprite)

        self.predicates.extend(
            ["(evaluate-interaction ?o1 ?o2 - Object)",
                "(regenerate-interaction ?o1 ?o2 - Object)"]
        )

        # PDDL specific
        self.predicates.extend(
            ["; To maintain order",
            "(turn-avatar)",
            "(turn-sprites)",
            "(turn-interactions)",

            "; For tile connections",
            "(connected-up ?c1 ?c2 - cell)",
            "(connected-down ?c1 ?c2 - cell)",
            "(connected-right ?c1 ?c2 - cell)",
            "(connected-left ?c1 ?c2 - cell)",

            "(at ?c - cell ?o - Object)",
            "(last-at ?c - cell ?o - Object)",

            "(object-dead ?o - Object)"]
        )

    # -------------------------------------------------------------------------

    def assign_functions(self):
        pass

    # -------------------------------------------------------------------------

    def assign_actions(self):
        """ Calls the different actions generators """

        # PDDL specific actions
        end_turn_interactions = Action(
            "END-TURN-INTERACTIONS", # Name
            [], # Parameters
            ["(turn-interactions)", 
            """(not 
				(exists (?x - Object ?y - Object ?c - cell) 
					(and
						(not (= ?x ?y))
						(at ?c ?x)
						(at ?c ?y)
					)
				)
			)"""], # Preconditions
            ["; Restart turn",
            "(turn-avatar)",
            "(not (turn-sprites))",
			"(not (turn-interactions))"], # Effects
        )
        self.actions.append(end_turn_interactions)


        predicates = []
        for sp in self.spritesPDDL:
            predicates.extend(sp.predicates)

        # Get the sprites predicates (turn-...)
        turn_predicates = [p for p in predicates if "(turn-" in p]

        # Get the sprites predicates (finished-turn-...)
        finished_predicates = [p for p in predicates if "(finished-turn-" in p]

        # Negate them and append last predicate
        negated_finished_predicates = ["(not " +  p + ")" for p in finished_predicates]
        negated_finished_predicates.append("(turn-interactions)")

        self.actions.append(Action(
            "TURN-SPRITES",
            [],
            ["(turn-sprites)"],
            turn_predicates
        )

        self.actions.append(Action(
            "END-TURN-SPRITES",
            [],
            finished_predicates,
            negated_finished_predicates
        )


        # Getting specific avatar actions
        avatar_actions = self.avatarPDDL.actions
        self.actions.extend(avatar_actions)

        # And one for each deterministic movable object
        for obj in self.sprites:
            partner = self.find_partner(obj)
            actions = SpritePDDL(obj, self.hierarchy, partner).actions

            if actions:
                self.actions.extend(actions)

        # And one for each interaction
        for interaction in self.interactions:
            sprite = self.find_sprite_by_name(interaction.sprite_name)
            partner = self.find_sprite_by_name(interaction.partner_name)
            self.actions.extend(
                InteractionActions(interaction, sprite, partner, self.hierarchy).actions
            )

    # -------------------------------------------------------------------------
