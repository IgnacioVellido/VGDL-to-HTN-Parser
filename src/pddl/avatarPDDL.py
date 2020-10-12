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

    def __init__(self, avatar: "Sprite", hierarchy: dict, partner: "Sprite" = None):
        self.avatar = avatar
        self.hierarchy = hierarchy
        self.partner = partner

        self.tasks = []
        self.methods = []
        self.actions = []
        self.predicates = []
        self.level_predicates = []

        self.get_actions()
        self.get_methods()
        self.get_tasks()
        self.get_predicates()
        self.get_level_predicates()

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def get_actions(self):
        self.actions = AvatarActions(self.avatar, self.hierarchy, self.partner).actions

    # -------------------------------------------------------------------------

    def get_level_predicates(self):
        self.level_predicates = AvatarLevelPredicates(self.avatar).level_predicates

    # -------------------------------------------------------------------------

    def get_methods(self):
        for action in self.actions:
            name = action.name.lower()

            # Getting the parameters (only the name, not the type)
            parameters = ""
            for p in action.parameters:
                parameters += " ?" + p[0]

            m_action = "(" + action.name + parameters + ")"

            m = Method(name, [], [m_action])

            self.methods.append(m)

    # -------------------------------------------------------------------------

    def get_predicates(self):
        self.predicates = AvatarPredicates(self.avatar, self.partner).predicates

    # -------------------------------------------------------------------------

    def get_tasks(self):
        """ Read parameters of each action and remove duplicates, produce task 
        (only one) including previous methods """

        # Getting the parameters from the actions
        parameters = []
        included_parameters = []  # To check for duplicates

        for action in self.actions:
            for p in action.parameters:
                if p[1] not in included_parameters:
                    included_parameters.append(p[1])

                    parameters.append([p[0], p[1]])

        self.task = Task("turn_avatar", parameters, self.methods)


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

    def __init__(self, avatar: "Sprite", hierarchy: dict, partner: "Sprite"):
        self.avatar = avatar
        self.hierarchy = hierarchy
        self.partner = partner

        self.actions = []
        self.get_actions()

        # MAYBE NEEDS self BEFORE EACH FUNCTIONS
        # Dict with the functions needed for each avatar
        avatar_action_list = {
            # Can't move but can use object
            "AimedAvatar" : [turn_up, turn_down, turn_left, turn_right, use, nil],

            # This avatar should have ammo !!!!!!!!!!
            # Always same orientation, can move horizontally and use object  
            "FlakAvatar"  : [move_left, move_right, use, nil],

            # Always same orientation, can only move left or right
            "HorizontalAvatar": [move_left, move_right, nil],

            # Always same orientation, can move in any direction
            # This avatar don't have orientation, so it can move freely
            "MovingAvatar" : [move_up, move_down, move_left, move_right, turn_up, turn_down, turn_left, turn_right, nil],

            # ONLY GVGAI
            "OngoingShootAvatar": [],

            # ONLY GVGAI
            "OngoingTurningAvatar" : [],

            # Can move and aim in any direction, can't use object
            "OrientedAvatar" : [move_up, move_down, move_left, move_right, turn_up, turn_down, turn_left, turn_right, nil],

            # Can move and aim in any direction, can use object
            "ShootAvatar" : [move_up, move_down, move_left, move_right, turn_up, turn_down, turn_left, turn_right, use, nil],

            # Always same orientation, can only move up or down
            "VerticalAvatar" : [move_up, move_down]
        }

        get_actions(avatar_action_list[self.avatar.stype])

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def get_actions(self, action_list):
      """ Return a list of actions depending of the avatar. """
        for function in action_list:
            self.actions.append(function())

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def move_up(self):
        name = "AVATAR_MOVE_UP"
        parameters = [["a", self.avatar.stype], ["c_actual", "cell"], ["c_last", "cell"], ["c_next", "cell"]]

        # can-move indicates that te avatar has the ability to move in that direction
        preconditions = ["(turn-avatar)", "(can-move-up ?a)", "(oriented-up ?a)", 
                         "(at ?c_actual ?a)", "(last-at ?c_last ?a)",
                         "(connected-up ?c_actual ?c_next)"]

        effects = ["(not (last-at ?c_last ?a))", "(last-at ?c_actual ?a)",
                    "(not (at ?c_actual ?a))", "(at ?c_next ?a)", 
                    "(not (turn-avatar)", "(turn-sprites)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def move_down(self):
        name = "AVATAR_MOVE_DOWN"
        parameters = [["a", self.avatar.stype], ["c_actual", "cell"], ["c_last", "cell"], ["c_next", "cell"]]

        # can-move indicates that te avatar has the ability to move in that direction
        preconditions = ["(turn-avatar)", "(can-move-down ?a)", "(oriented-down ?a)", 
                         "(at ?c_actual ?a)", "(last-at ?c_last ?a)",
                         "(connected-down ?c_actual ?c_next)"]
        effects = ["(not (last-at ?c_last ?a))", "(last-at ?c_actual ?a)",
                    "(not (at ?c_actual ?a))", "(at ?c_next ?a)", 
                    "(not (turn-avatar)", "(turn-sprites)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def move_left(self):
        name = "AVATAR_MOVE_LEFT"
        parameters = [["a", self.avatar.stype], ["c_actual", "cell"], ["c_last", "cell"], ["c_next", "cell"]]

        # can-move indicates that te avatar has the ability to move in that direction
        preconditions = ["(turn-avatar)", "(can-move-left ?a)", "(oriented-left ?a)", 
                         "(at ?c_actual ?a)", "(last-at ?c_last ?a)",
                         "(connected-left ?c_actual ?c_next)"]
        effects = ["(not (last-at ?c_last ?a))", "(last-at ?c_actual ?a)",
                    "(not (at ?c_actual ?a))", "(at ?c_next ?a)", 
                    "(not (turn-avatar)", "(turn-sprites)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def move_right(self):
        name = "AVATAR_MOVE_RIGHT"
        parameters = [["a", self.avatar.stype], ["c_actual", "cell"], ["c_last", "cell"], ["c_next", "cell"]]

        # can-move indicates that te avatar has the ability to move in that direction
        preconditions = ["(turn-avatar)", "(can-move-right ?a)", "(oriented-right ?a)", 
                         "(at ?c_actual ?a)", "(last-at ?c_last ?a)",
                         "(connected-right ?c_actual ?c_next)"]
        effects = ["(not (last-at ?c_last ?a))", "(last-at ?c_actual ?a)",
                    "(not (at ?c_actual ?a))", "(at ?c_next ?a)", 
                    "(not (turn-avatar)", "(turn-sprites)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # This method should only be called if the avatar can turn
    def turn_up(self):
        name = "AVATAR_TURN_UP"
        parameters = [["a", self.avatar.stype]]

        # If not (can-change-orientation ?a), the avatar cannot use this action
        # preconditions = ["(turn-avatar)", "(can-change-orientation ?a)","(not (oriented-up ?a))"]
        # can-change-orientation maybe not needed
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

        effects = [effect_down, effect_right, effect_left, "(oriented-up ?a)", "(not (turn-avatar)", "(turn-sprites)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def turn_down(self):
        name = "AVATAR_TURN_DOWN"
        parameters = [["a", self.avatar.stype]]

        # If not (can-change-orientation ?a), the avatar cannot use this action
        # preconditions = ["(turn-avatar)", "(can-change-orientation ?a)","(not (oriented-down ?a))"]
        # can-change-orientation maybe not needed
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

        effects = [effect_left, effect_right, effect_up, "(oriented-down ?a)", "(not (turn-avatar)", "(turn-sprites)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def turn_left(self):
        name = "AVATAR_TURN_LEFT"
        parameters = [["a", self.avatar.stype]]

        # If not (can-change-orientation ?a), the avatar cannot use this action
        # preconditions = ["(turn-avatar)", "(can-change-orientation ?a)","(not (oriented-left ?a))"]
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

        effects = [effect_down, effect_right, effect_up, "(oriented-left ?a)", "(not (turn-avatar)", "(turn-sprites)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def turn_right(self):
        name = "AVATAR_TURN_RIGHT"
        parameters = [["a", self.avatar.stype]]

        # If not (can-change-orientation ?a), the avatar cannot use this action
        # preconditions = ["(turn-avatar)", "(can-change-orientation ?a)","(not (oriented-right ?a))"]
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

        effects = [effect_down, effect_left, effect_up, "(oriented-right ?a)", "(not (turn-avatar)", "(turn-sprites)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # can-use is a predicate that should not be active in case there is no ammo
    def use_up(self):
        """ Generates the partner object in front of the avatar (UP)

        partner:     Sprite that is generated
        """
        if self.partner == None:
            raise TypeError('Argument "partner" is not defined')

        name = "AVATAR_USE_UP"
        parameters = [["a", self.avatar.stype], ["p", self.partner.name], ["c_actual", "cell"], ["c_up", "cell"]]
        preconditions = ["(turn-avatar)", "(can-use ?a ?p)", "(at ?c_actual ?a)", "(oriented-up ?a)", "(connected-up ?c_actual ?c_up)"]

        effects = ["(at ?c_up ?p)", "(not (turn-avatar)", "(turn-sprites)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # MAYBE SOME AVATAR DON'T HAVE ORIENTATION BUT CAN USE - CAREFULL

    # can-use is a predicate that should not be active in case there is no ammo
    def use_down(self):
        """ Generates the partner object in front of the avatar (UP)

        partner:     Sprite that is generated
        """
        if self.partner == None:
            raise TypeError('Argument "partner" is not defined')

        name = "AVATAR_USE_DOWN"
        parameters = [["a", self.avatar.stype], ["p", self.partner.name], ["c_actual", "cell"], ["c_down", "cell"]]
        preconditions = ["(turn-avatar)", "(can-use ?a ?p)", "(at ?c_actual ?a)", "(oriented-down ?a)", "(connected-down ?c_actual ?c_down)"]

        effects = ["(at ?c_down ?p)", "(not (turn-avatar)", "(turn-sprites)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # can-use is a predicate that should not be active in case there is no ammo
    def use_left(self):
        """ Generates the partner object in front of the avatar (UP)

        partner:     Sprite that is generated
        """
        if self.partner == None:
            raise TypeError('Argument "partner" is not defined')

        name = "AVATAR_USE_LEFT"
        parameters = [["a", self.avatar.stype], ["p", self.partner.name], ["c_actual", "cell"], ["c_left", "cell"]]
        preconditions = ["(turn-avatar)", "(can-use ?a ?p)", "(at ?c_actual ?a)", "(oriented-left ?a)", "(connected-left ?c_actual ?c_left)"]

        effects = ["(at ?c_left ?p)", "(not (turn-avatar)", "(turn-sprites)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # can-use is a predicate that should not be active in case there is no ammo
    def use_right(self):
        """ Generates the partner object in front of the avatar (UP)

        partner:     Sprite that is generated
        """
        if self.partner == None:
            raise TypeError('Argument "partner" is not defined')

        name = "AVATAR_USE_RIGHT"
        parameters = [["a", self.avatar.stype], ["p", self.partner.name], ["c_actual", "cell"], ["c_right", "cell"]]
        preconditions = ["(turn-avatar)", "(can-use ?a ?p)", "(at ?c_actual ?a)", "(oriented-right ?a)", "(connected-right ?c_actual ?c_right)"]

        effects = ["(at ?c_right ?p)", "(not (turn-avatar)", "(turn-sprites)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # Probably will not work
    def nil(self):
        """ Avatar doesn't do anything """
        name = "AVATAR_NIL"
        parameters = [["a", self.avatar.stype]]
        preconditions = ["(turn-avatar)"]
        effects = ["(not (turn-avatar)", "(turn-sprites)"]

        return Action(name, parameters, preconditions, effects)


###############################################################################
# -----------------------------------------------------------------------------
###############################################################################


class AvatarPredicates:
    """ Returns different predicates depending of the avatar """

    def __init__(self, avatar: "Sprite", partner: "Sprite" = None):
        self.avatar = avatar
        self.partner = partner

        self.predicates = []
        self.get_predicates()

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def get_predicates(self):
        """ Return a list of predicates depending of the avatar """

        # Can't move but can use object
        if self.avatar.stype == "AimedAvatar":
            self.predicates.append("(can-use ?a - " + self.avatar.stype + " ?p - " + self.partner.name + ")")
            self.predicates.append(
                "(can-change-orientation ?a - " + self.avatar.stype + ")"
            )

        # This avatar should have ammo !!!!
        # Always same orientation, can move horizontally and use object
        if self.avatar.stype == "FlakAvatar":
            self.predicates.append("(can-move-left ?a - " + self.avatar.stype + ")")
            self.predicates.append("(can-move-right ?a - " + self.avatar.stype + ")")
            self.predicates.append("(can-use ?a - " + self.avatar.stype + " ?p - " + self.partner.name + ")")

        # Always same orientation, can only move left or right
        if self.avatar.stype == "HorizontalAvatar":
            self.predicates.append("(can-move-left ?a - " + self.avatar.stype + ")")
            self.predicates.append("(can-move-right ?a - " + self.avatar.stype + ")")

        # Always same orientation, can move in any direction
        if self.avatar.stype == "MovingAvatar":
            self.predicates.append("(can-move-up ?a - " + self.avatar.stype + ")")
            self.predicates.append("(can-move-down ?a - " + self.avatar.stype + ")")
            self.predicates.append("(can-move-left ?a - " + self.avatar.stype + ")")
            self.predicates.append("(can-move-right ?a - " + self.avatar.stype + ")")

        # ONLY GVGAI
        if self.avatar.stype == "OngoingShootAvatar":
            pass

        # ONLY GVGAI
        if self.avatar.stype == "OngoingTurningAvatar":
            pass

        # Can move and aim in any direction
        if self.avatar.stype == "OrientedAvatar":
            self.predicates.append("(can-move-up ?a - " + self.avatar.stype + ")")
            self.predicates.append("(can-move-down ?a - " + self.avatar.stype + ")")
            self.predicates.append("(can-move-left ?a - " + self.avatar.stype + ")")
            self.predicates.append("(can-move-right ?a - " + self.avatar.stype + ")")
            self.predicates.append(
                "(can-change-orientation ?a - " + self.avatar.stype + ")"
            )

        # Can move and aim in any direction, can use object
        if self.avatar.stype == "ShootAvatar":
            self.predicates.append("(can-move-up ?a - " + self.avatar.stype + ")")
            self.predicates.append("(can-move-down ?a - " + self.avatar.stype + ")")
            self.predicates.append("(can-move-left ?a - " + self.avatar.stype + ")")
            self.predicates.append("(can-move-right ?a - " + self.avatar.stype + ")")
            self.predicates.append(
                "(can-change-orientation ?a - " + self.avatar.stype + ")"
            )
            self.predicates.append("(can-use ?a - " + self.avatar.stype + " ?p - " + self.partner.name + ")")

        # Always same orientation, can only move up or down
        if self.avatar.stype == "VerticalAvatar":
            self.predicates.append("(can-move-up ?a - " + self.avatar.stype + ")")
            self.predicates.append("(can-move-down ?a - " + self.avatar.stype + ")")


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

    def get_level_predicates(self):
        """ Return a list of predicates depending of the avatar """
        self.level_predicates.append("(oriented-up ?a)")

        # Can't move but can use object
        if self.avatar.stype == "AimedAvatar":
            self.level_predicates.append("(can-use ?a partner)")
            self.level_predicates.append("(can-change-orientation ?a)")

        # This avatar should have ammo !!!!
        # Always same orientation, can move horizontally and use object
        if self.avatar.stype == "FlakAvatar":
            self.level_predicates.append("(can-move-left ?a)")
            self.level_predicates.append("(can-move-right ?a)")
            self.level_predicates.append("(can-use ?a partner)")

        # Always same orientation, can only move left or right
        if self.avatar.stype == "HorizontalAvatar":
            self.level_predicates.append("(can-move-left ?a)")
            self.level_predicates.append("(can-move-right ?a)")

        # Always same orientation, can move in any direction
        if self.avatar.stype == "MovingAvatar":
            self.level_predicates.append("(can-move-up ?a)")
            self.level_predicates.append("(can-move-down ?a)")
            self.level_predicates.append("(can-move-left ?a)")
            self.level_predicates.append("(can-move-right ?a)")

        # ONLY GVGAI
        if self.avatar.stype == "OngoingShootAvatar":
            pass

        # ONLY GVGAI
        if self.avatar.stype == "OngoingTurningAvatar":
            pass

        # Can move and aim in any direction
        if self.avatar.stype == "OrientedAvatar":
            self.level_predicates.append("(can-move-up ?a)")
            self.level_predicates.append("(can-move-down ?a)")
            self.level_predicates.append("(can-move-left ?a)")
            self.level_predicates.append("(can-move-right ?a)")
            self.level_predicates.append("(can-change-orientation ?a)")

        # Can move and aim in any direction, can use object
        if self.avatar.stype == "ShootAvatar":
            self.level_predicates.append("(can-move-up ?a)")
            self.level_predicates.append("(can-move-down ?a)")
            self.level_predicates.append("(can-move-left ?a)")
            self.level_predicates.append("(can-move-right ?a)")
            self.level_predicates.append("(can-change-orientation ?a)")
            self.level_predicates.append("(can-use ?a partner)")

        # Always same orientation, can only move up or down
        if self.avatar.stype == "VerticalAvatar":
            self.level_predicates.append("(can-move-up ?a)")
            self.level_predicates.append("(can-move-down ?a )")
