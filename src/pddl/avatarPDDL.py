###############################################################################
# avatarPDDL.py
# Ignacio Vellido Expósito
# 28/09/2020
#
# Multiple classes defining parts of a PDDL domain for an avatar
###############################################################################

from pddl.typesPDDL import *

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################


class AvatarPDDL:
    """ Class that encapsulate the generation of PDDL domain structures 
    for the avatar
    
    Atributes:
        avatar           - SpriteVGDL
        partner          - SpriteVGDL
        hierarchy        - Dict<String,String>
    """

    def __init__(
        self, 
        avatar: "Sprite", 
        hierarchy: dict, 
        stepbacks: list, 
        killIfHasLess: list,
        killIfOtherHasMore: list,
        partner: "Sprite" = None
    ):
        self.avatar = avatar
        self.hierarchy = hierarchy
        self.stepbacks = stepbacks
        self.killIfHasLess = killIfHasLess
        self.killIfOtherHasMore = killIfOtherHasMore
        self.partner = partner

        self.tasks = []     # Empty
        self.methods = []   # Empty
        self.actions = []
        self.predicates = []
        self.level_predicates = []


        # Remove killIfOtherHasMore sprites from stepbacks
        for o in self.killIfOtherHasMore:
            if o[1] in self.stepbacks:
                self.stepbacks.remove(o[1])

        self.get_actions()
        self.get_predicates()
        self.get_level_predicates()

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def get_actions(self):
        self.actions = AvatarActions(self.avatar, self.hierarchy, self.stepbacks, 
                                        self.killIfHasLess, self.killIfOtherHasMore,
                                        self.partner).actions

    # -------------------------------------------------------------------------

    def get_level_predicates(self):
        self.level_predicates = AvatarLevelPredicates(self.avatar).level_predicates

    # -------------------------------------------------------------------------

    def get_predicates(self):
        self.predicates = AvatarPredicates(self.avatar, self.stepbacks, 
                                            self.killIfHasLess, self.killIfOtherHasMore, self.partner).predicates

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################


class AvatarActions:
    """ Returns different actions depending of the avatar 

    Atributes:
        avatar  - SpriteVGDL
        partner - SpriteVGDL
                    If ACTION_USE is available for the avatar, 'partner' is the 
                    sprite that is produced
        actions - List<ActionPDDL>
    """

    def __init__(
        self, 
        avatar: "Sprite", 
        hierarchy: dict, 
        stepbacks: list, 
        killIfHasLess: list,
        killIfOtherHasMore: list,
        partner: "Sprite"
    ):
        self.avatar = avatar
        self.hierarchy = hierarchy
        self.stepbacks = stepbacks
        self.killIfHasLess = killIfHasLess
        self.killIfOtherHasMore = killIfOtherHasMore
        self.partner = partner

        # stepbacks and killIfOtherHasMore intersects.
        # Remove common sprites
        for o in stepbacks:
            if o[0] in stepbacks:
                self.stepbacks.remove()

        self.actions = []

        # Dict with the functions needed for each avatar
        avatar_action_list = {
            # Can't move but can turn and use object over itself
            "AimedAvatar" : [self.turn_up, self.turn_down, self.turn_left, self.turn_right, self.use_up, self.use_down, self.use_left, self.use_right], # self.nil],

            # NOT SUPPORTED
            # This avatar should have ammo !!!!!!!!!!
            # Always same orientation, can move horizontally and use object
            # "FlakAvatar"  : [self.move_left, self.move_right, self.use_center] # self.nil],

            # Always same orientation, can only move left or right
            "HorizontalAvatar": [self.move_left, self.move_right], # self.nil],

            # Always same orientation, can move in any direction
            # This avatar doesn't have orientation, so it can move freely
            "MovingAvatar" : [self.move_up, self.move_down, self.move_left, self.move_right], # self.nil],

            # Can move and turn in any direction
            "OrientedAvatar" : [self.move_up, self.move_down, self.move_left, self.move_right, self.turn_up, self.turn_down, self.turn_left, self.turn_right], # self.nil],

            # Can move and turn in any direction, can use object in the 4 directions
            "ShootAvatar" : [self.move_up, self.move_down, self.move_left, self.move_right, self.turn_up, self.turn_down, self.turn_left, self.turn_right, self.use_up, self.use_down, self.use_left, self.use_right], # self.nil],

            # Always same orientation, can only move up or down
            "VerticalAvatar" : [self.move_up, self.move_down]
        }

        self.get_actions(avatar_action_list.get(self.avatar.stype, []))

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def get_actions(self, action_list):
        """ Stores in self.actions the actions defined """
        for function in action_list:
            act = function()
            # If case Action is not returned
            if act:
                self.actions.append(function())

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    # DONE - Needed stepback objects
    def move_up(self):
        name = "AVATAR_ACTION_MOVE_UP"
        parameters = [["a", self.avatar.stype], ["x", "num"], ["y", "num"], ["new_y", "num"]]

        # can-move indicates that te avatar has the ability to move in that direction
        preconditions = ["(turn-avatar)", "(or (oriented-up ?a) (oriented-none ?a))",
                         "(at ?x ?y ?a)",
                         "(previous ?y ?new_y)"]

        # Add stepback objects
        for o in self.stepbacks:
            preconditions.append("(not (is-" + o + " ?x ?new_y))")
        
        # Add killIfHasLess
        # o[0] -> type of cell
        # o[1] -> resource needed
        for o in self.killIfHasLess:
            preconditions.append("""(or
                            (and 
                                (is-""" + o[0] + """ ?x ?new_y)
                                (not (got-resource-""" + o[1] + """ n0))
                            )
                            (not (is-""" + o[0] + """ ?x ?new_y))
                        )""")

        # Add killIfOtherHasMore
        # o[0] -> type of cell
        # o[1] -> resource needed
        # o[2] -> resource limit
        for o in self.killIfOtherHasMore:
            preconditions.append("""(or
                            (not (is-""" + o[0] + """ ?x ?new_y))
                            (and 
                                (is-""" + o[0] + """ ?x ?new_y)
                                (got-resource-""" + o[1] + """ n""" + o[2] + """)
                            )
                        )""")
        
        effects = [
                    "(not (at ?x ?y ?a))", "(at ?x ?new_y ?a)", 
                    "(not (turn-avatar))", "(turn-interactions)", """; Change orientation
					(when
                        (oriented-down ?a )
                        (not (oriented-down ?a))
                    )
					
                    (when
                        (oriented-right ?a )
                        (not (oriented-right ?a))
                    )
					
                    (when
                        (oriented-left ?a )
                        (not (oriented-left ?a))
                    )
					(oriented-up ?a)"""]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # DONE - Needed stepback objects
    def move_down(self):
        name = "AVATAR_ACTION_MOVE_DOWN"
        parameters = [["a", self.avatar.stype], ["x", "num"], ["y", "num"], ["new_y", "num"]]

        # can-move indicates that te avatar has the ability to move in that direction
        preconditions = ["(turn-avatar)", "(or (oriented-down ?a) (oriented-none ?a))",
                         "(at ?x ?y ?a)",
                         "(next ?y ?new_y)"]

        # Add stepback objects
        for o in self.stepbacks:
            preconditions.append("(not (is-" + o + " ?x ?new_y))")

        # Add killIfHasLess
        # o[0] -> type of cell
        # o[1] -> resource needed
        for o in self.killIfHasLess:
            preconditions.append("""(or
                            (and 
                                (is-""" + o[0] + """ ?x ?new_y)
                                (not (got-resource-""" + o[1] + """ n0))
                            )
                            (not (is-""" + o[0] + """ ?x ?new_y))
                        )""")

        # Add killIfOtherHasMore
        # o[0] -> type of cell
        # o[1] -> resource needed
        # o[2] -> resource limit
        for o in self.killIfOtherHasMore:
            preconditions.append("""(or
                            (not (is-""" + o[0] + """ ?x ?new_y))
                            (and 
                                (is-""" + o[0] + """ ?x ?new_y)
                                (got-resource-""" + o[1] + """ n""" + o[2] + """)
                            )
                        )""")
        
        effects = [
                    "(not (at ?x ?y ?a))", "(at ?x ?new_y ?a)", 
                    "(not (turn-avatar))", "(turn-interactions)", """; Change orientation
					(when
                        (oriented-up ?a )
                        (not (oriented-up ?a))
                    )					
                    (when
                        (oriented-right ?a )
                        (not (oriented-right ?a))
                    )					
                    (when
                        (oriented-left ?a )
                        (not (oriented-left ?a))
                    )
					(oriented-down ?a)"""]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # DONE
    def move_left(self):
        name = "AVATAR_ACTION_MOVE_LEFT"
        parameters = [["a", self.avatar.stype], ["x", "num"], ["y", "num"], ["new_x", "num"]]

        # can-move indicates that te avatar has the ability to move in that direction
        preconditions = ["(turn-avatar)", "(or (oriented-left ?a) (oriented-none ?a))", 
                         "(at ?x ?y ?a)",
                         "(previous ?x ?new_x)"]

        # Add stepback objects
        for o in self.stepbacks:
            preconditions.append("(not (is-" + o + " ?new_x ?y))")


        # Add killIfHasLess
        # o[0] -> type of cell
        # o[1] -> resource needed
        for o in self.killIfHasLess:
            preconditions.append("""(or
                            (and 
                                (is-""" + o[0] + """ ?new_x ?y)
                                (not (got-resource-""" + o[1] + """ n0))
                            )
                            (not (is-""" + o[0] + """ ?new_x ?y))
                        )""")

        # Add killIfOtherHasMore
        # o[0] -> type of cell
        # o[1] -> resource needed
        # o[2] -> resource limit
        for o in self.killIfOtherHasMore:
            preconditions.append("""(or
                            (not (is-""" + o[0] + """ ?new_x ?y))
                            (and 
                                (is-""" + o[0] + """ ?new_x ?y)
                                (got-resource-""" + o[1] + """ n""" + o[2] + """)
                            )
                        )""")

        effects = [
                    "(not (at ?x ?y ?a))", "(at ?new_x ?y ?a)", 
                    "(not (turn-avatar))", "(turn-interactions)", """; Change orientation
                    (when
                        (oriented-up ?a )
                        (not (oriented-up ?a))
                    )
					(when
                        (oriented-down ?a )
                        (not (oriented-down ?a))
                    )					
                    (when
                        (oriented-right ?a )
                        (not (oriented-right ?a))
                    )					
					(oriented-left ?a)"""]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # DONE
    def move_right(self):
        name = "AVATAR_ACTION_MOVE_RIGHT"
        parameters = [["a", self.avatar.stype], ["x", "num"], ["y", "num"], ["new_x", "num"]]

        # can-move indicates that te avatar has the ability to move in that direction
        preconditions = ["(turn-avatar)", "(or (oriented-right ?a) (oriented-none ?a))", 
                         "(at ?x ?y ?a)",
                         "(next ?x ?new_x)"]

        # Add stepback objects
        for o in self.stepbacks:
            preconditions.append("(not (is-" + o + " ?new_x ?y))")

        # Add killIfHasLess
        # o[0] -> type of cell
        # o[1] -> resource needed
        for o in self.killIfHasLess:
            preconditions.append("""(or
                            (and 
                                (is-""" + o[0] + """ ?new_x ?y)
                                (not (got-resource-""" + o[1] + """ n0))
                            )
                            (not (is-""" + o[0] + """ ?new_x ?y))
                        )""")

        # Add killIfOtherHasMore
        # o[0] -> type of cell
        # o[1] -> resource needed
        # o[2] -> resource limit
        for o in self.killIfOtherHasMore:
            preconditions.append("""(or
                            (not (is-""" + o[0] + """ ?new_x ?y))
                            (and 
                                (is-""" + o[0] + """ ?new_x ?y)
                                (got-resource-""" + o[1] + """ n""" + o[2] + """)
                            )
                        )""")

        effects = [
                    "(not (at ?x ?y ?a))", "(at ?new_x ?y ?a)", 
                    "(not (turn-avatar))", "(turn-interactions)", """; Change orientation
                    (when
                        (oriented-up ?a )
                        (not (oriented-up ?a))
                    )					
					(when
                        (oriented-down ?a )
                        (not (oriented-down ?a))
                    )					
                    (when
                        (oriented-left ?a )
                        (not (oriented-left ?a))
                    )
					(oriented-right ?a)"""]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # DONE
    # This method should only be called if the avatar can turn
    def turn_up(self):
        name = "AVATAR_ACTION_TURN_UP"
        parameters = [["a", self.avatar.stype]]

        preconditions = ["(turn-avatar)", "(not (oriented-up ?a))"]

        effect_down = """
                    (when
                        (oriented-down ?a )
                        (not (oriented-down ?a))
                    )"""
        effect_left = """
                    (when
                        (oriented-left ?a )
                        (not (oriented-left ?a))
                    )"""
        effect_right = """
                    (when
                        (oriented-right ?a )
                        (not (oriented-right ?a))
                    )"""

        effects = [effect_down, effect_right, effect_left, "(oriented-up ?a)", "(not (turn-avatar))", "(turn-interactions)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # DONE
    def turn_down(self):
        name = "AVATAR_ACTION_TURN_DOWN"
        parameters = [["a", self.avatar.stype]]

        preconditions = ["(turn-avatar)", "(not (oriented-down ?a))"]

        effect_up = """
                    (when
                        (oriented-up ?a )
                        (not (oriented-up ?a))
                    )"""
        effect_left = """
                    (when
                        (oriented-left ?a )
                        (not (oriented-left ?a))
                    )"""
        effect_right = """
                    (when
                        (oriented-right ?a )
                        (not (oriented-right ?a))
                    )"""

        effects = [effect_left, effect_right, effect_up, "(oriented-down ?a)", "(not (turn-avatar))", "(turn-interactions)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # DONE
    def turn_left(self):
        name = "AVATAR_ACTION_TURN_LEFT"
        parameters = [["a", self.avatar.stype]]

        preconditions = ["(turn-avatar)", "(not (oriented-left ?a))"]

        effect_down = """
                    (when
                        (oriented-down ?a )
                        (not (oriented-down ?a))
                    )"""
        effect_up = """
                    (when
                        (oriented-up ?a )
                        (not (oriented-up ?a))
                    )"""
        effect_right = """
                    (when
                        (oriented-right ?a )
                        (not (oriented-right ?a))
                    )"""

        effects = [effect_down, effect_right, effect_up, "(oriented-left ?a)", "(not (turn-avatar))", "(turn-interactions)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # DONE
    def turn_right(self):
        name = "AVATAR_ACTION_TURN_RIGHT"
        parameters = [["a", self.avatar.stype]]

        preconditions = ["(turn-avatar)", "(not (oriented-right ?a))"]

        effect_down = """
                    (when
                        (oriented-down ?a )
                        (not (oriented-down ?a))
                    )"""
        effect_up = """
                    (when
                        (oriented-up ?a )
                        (not (oriented-up ?a))
                    )"""
        effect_left = """
                    (when
                        (oriented-left ?a )
                        (not (oriented-left ?a))
                    )"""

        effects = [effect_down, effect_left, effect_up, "(oriented-right ?a)", "(not (turn-avatar))", "(turn-interactions)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # DONE
    def use_center(self):
        """ Generates the partner object in the same tile as the avatar

        partner:     Sprite that is generated
        """
        if self.partner == None:
            raise TypeError('Argument "partner" is not defined')

        name = "AVATAR_ACTION_USE_CENTER"
        parameters = [["a", self.avatar.stype], ["p", self.partner.name], ["x", "num"], ["y", "num"]]
        preconditions = ["(turn-avatar)", "(at ?x ?y ?a)"]

        effects = ["(at ?x ?y ?p)", "(not (turn-avatar))", "(turn-interactions)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # DONE
    def use_up(self):
        """ Generates the partner object in front of the avatar (UP)

        partner:     Sprite that is generated
        """
        if self.partner == None:
            raise TypeError('Argument "partner" is not defined')

        name = "AVATAR_ACTION_USE_UP"
        parameters = [["a", self.avatar.stype], ["p", self.partner.name], ["x", "num"], ["y", "num"], ["new_y", "num"]]
        preconditions = ["(turn-avatar)", "(at ?x ?y ?a)", "(oriented-up ?a)", "(previous ?y ?new_y)"]

        effects = ["(at ?x ?new_y ?p)", "(not (turn-avatar))", "(turn-interactions)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # DONE
    def use_down(self):
        """ Generates the partner object in front of the avatar (UP)

        partner:     Sprite that is generated
        """
        if self.partner == None:
            raise TypeError('Argument "partner" is not defined')

        name = "AVATAR_ACTION_USE_DOWN"
        parameters = [["a", self.avatar.stype], ["p", self.partner.name], ["x", "num"], ["y", "num"], ["new_y", "num"]]
        preconditions = ["(turn-avatar)", "(at ?x ?y ?a)", "(oriented-down ?a)", "(next ?y ?new_y)"]

        effects = ["(at ?x ?new_y ?p)", "(not (turn-avatar))", "(turn-interactions)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # DONE
    def use_left(self):
        """ Generates the partner object in front of the avatar (UP)

        partner:     Sprite that is generated
        """
        if self.partner == None:
            raise TypeError('Argument "partner" is not defined')

        name = "AVATAR_ACTION_USE_LEFT"
        parameters = [["a", self.avatar.stype], ["p", self.partner.name], ["x", "num"], ["y", "num"], ["new_x", "num"]]
        preconditions = ["(turn-avatar)", "(at ?x ?y ?a)", "(oriented-left ?a)", "(previous ?x ?new_x)"]

        effects = ["(at ?new_x ?y ?p)", "(not (turn-avatar))", "(turn-interactions)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # DONE
    def use_right(self):
        """ Generates the partner object in front of the avatar (UP)

        partner:     Sprite that is generated
        """
        if self.partner == None:
            raise TypeError('Argument "partner" is not defined')

        name = "AVATAR_ACTION_USE_RIGHT"
        parameters = [["a", self.avatar.stype], ["p", self.partner.name], ["x", "num"], ["y", "num"], ["new_x", "num"]]
        preconditions = ["(turn-avatar)", "(at ?x ?y ?a)", "(oriented-right ?a)", "(next ?x ?new_x)"]

        effects = ["(at ?new_x ?y ?p)", "(not (turn-avatar))", "(turn-interactions)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # DONE
    def nil(self):
        """ Avatar doesn't do anything """
        name = "AVATAR_ACTION_NIL"
        parameters = [["a", self.avatar.stype]]
        preconditions = ["(turn-avatar)"]
        effects = ["(not (turn-avatar))", "(turn-interactions)"]

        return Action(name, parameters, preconditions, effects)


###############################################################################
# -----------------------------------------------------------------------------
###############################################################################


class AvatarPredicates:
    """ Returns different predicates depending of the avatar """

    def __init__(self, avatar: "Sprite", stepbacks: list, killIfHasLess: list, killIfOtherHasMore: list,
                    partner: "Sprite" = None):
        self.avatar = avatar
        self.stepbacks = stepbacks
        self.killIfHasLess = killIfHasLess
        self.killIfOtherHasMore = killIfOtherHasMore
        self.partner = partner

        self.predicates = []
        self.get_predicates()

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def get_predicates(self):
        """ Return a list of predicates depending of the avatar """
        # To avoid errors in dict
        if not self.partner:
            partner_name = ""
        else:
            partner_name = self.partner.name


        # Dict with the predicates needed for each avatar
        avatar_predicates_list = {
            # Can't move but can use object
            "AimedAvatar" : [],

            # NOT SUPPORTED
            # This avatar should have ammo !!!!!!!!!!
            # Always same orientation, can move horizontally and use object  
            # "FlakAvatar"  : [],

            # Always same orientation, can only move left or right
            "HorizontalAvatar": [],

            # Always same orientation, can move in any direction
            # This avatar don't have orientation, so it can move freely
            "MovingAvatar" : [],

            # Can move and aim in any direction, can't use object
            "OrientedAvatar" : [],

            # Can move and aim in any direction, can use object
            "ShootAvatar" : [],

            # Always same orientation, can only move up or down
            "VerticalAvatar" : []
        }

        # Add stepback objects
        for o in self.stepbacks:
            self.predicates.append("(is-" + o + " ?x ?y - num)")
        for o in self.killIfHasLess:
            self.predicates.append("(is-" + o[0] + " ?x ?y - num)")
        for o in self.killIfOtherHasMore:
            self.predicates.append("(is-" + o[0] + " ?x ?y - num)")

        self.predicates.extend(avatar_predicates_list.get(self.avatar.stype, []))


###############################################################################
# -----------------------------------------------------------------------------
###############################################################################


class AvatarLevelPredicates:
    """ Returns different level predicates depending of the avatar """

    def __init__(self, avatar: "Sprite"):
        self.avatar = avatar

        self.level_predicates = []
        self.get_level_predicates()

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    # Avatar is defined as ?a to be substituted later for the real name
    def get_level_predicates(self):
        """ Return a list of predicates depending of the avatar """

        # Generic orientation for all avatars
        self.level_predicates.append("(oriented-up ?a)")

        # Dict with the predicates needed for each avatar
        avatar_levelPredicates_list = {
            # Can't move but can use object
            "AimedAvatar" : [],

            # NOT SUPPORTED
            # This avatar should have ammo !!!!!!!!!!
            # Always same orientation, can move horizontally and use object  
            # "FlakAvatar"  : [],

            # Always same orientation, can only move left or right
            "HorizontalAvatar": [],

            # Always same orientation, can move in any direction
            # This avatar don't have orientation, so it can move freely
            "MovingAvatar" : [],

            # Can move and aim in any direction, can't use object
            "OrientedAvatar" : [],

            # Can move and aim in any direction, can use object
            "ShootAvatar" : [],

            # Always same orientation, can only move up or down
            "VerticalAvatar" : []
        }

        self.level_predicates.extend(avatar_levelPredicates_list.get(self.avatar.stype, []))