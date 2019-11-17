###############################################################################
# avatar.py
# Ignacio Vellido Expósito
# 09/09/2019
# 
# Multiple classes defining parts of a HPDL domain for an avatar
###############################################################################

from hpdl.hpdlTypes import *

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class AvatarHPDL:
    """ Class that encapsulate the generation of HPDL domain structures 
    for the avatar """
    def __init__(self, avatar_name, avatar_type, partner=None):
        self.avatar_name = avatar_name
        self.avatar_type = avatar_type
        self.patner      = partner

        self.actions    = AvatarActions(avatar_name, avatar_type, partner).actions
        self.methods    = []
        self.get_methods()
        self.task       = None
        self.get_task()
        self.predicates = AvatarPredicates(avatar_name, avatar_type).predicates

    # -------------------------------------------------------------------------
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

    def get_task(self):
        """ Read parameters of each action and remove duplicates, produce task 
        (only one) including previous methods """

        # Getting the parameters from the actions
        parameters = []       
        included_parameters = []    # To check for duplicates    

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
        avatar_name
        avatar_type
        partner         Sprite object. 
                        If ACTION_USE is available for the avatar, 'partner' is the 
                        sprite that is produced
        actions         List of Action (depends of the avatar)
    """
    """ 
    Although we can declare same predicates for any kind of avatar, some
    will always be false, so, the reduce space in the domain we don't write 
    them 
    """
    def __init__(self, avatar_name, avatar_type, partner=None):
        self.avatar_name = avatar_name
        self.avatar_type = avatar_type
        self.partner     = partner

        self.actions = []
        self.get_actions()

    # Podrían juntarse para no repetir código pero lo haría menos legible
    def get_actions(self):
        """ Return a list of actions depending of the avatar.
        
        partner:    If ACTION_USE is available for the avatar, 'partner' is the 
                    sprite that is produced
        """

        # Can't move but can use object
        if self.avatar_type == "AimedAvatar":
            self.actions.append(self.turn_up())
            self.actions.append(self.turn_down())
            self.actions.append(self.turn_left())
            self.actions.append(self.turn_right())
            self.actions.append(self.use())

        # This avatar should have ammo !!!!!!!!!!
        # Always same orientation, can move horizontally and use object
        if self.avatar_type == "FlakAvatar":
            self.actions.append(self.move_left())
            self.actions.append(self.move_right())
            self.actions.append(self.use())

        # Always same orientation, can only move left or right
        if self.avatar_type == "HorizontalAvatar":
            self.actions.append(self.move_left())
            self.actions.append(self.move_right())

        # Always same orientation, can move in any direction
        if self.avatar_type == "MovingAvatar":
            self.actions.append(self.move_up())
            self.actions.append(self.move_down())
            self.actions.append(self.move_left())
            self.actions.append(self.move_right())

        # ONLY GVGAI
        if self.avatar_type == "OngoingShootAvatar":
            pass

        # ONLY GVGAI
        if self.avatar_type == "OngoingTurningAvatar":
            pass

        # Can move and aim in any direction, can't use object
        if self.avatar_type == "OrientedAvatar":
            self.actions.append(self.move_up())
            self.actions.append(self.move_down())
            self.actions.append(self.move_left())
            self.actions.append(self.move_right())
            self.actions.append(self.turn_up())
            self.actions.append(self.turn_down())
            self.actions.append(self.turn_left())
            self.actions.append(self.turn_right())
        
        # Can move and aim in any direction, can use object
        if self.avatar_type == "ShootAvatar":
            self.actions.append(self.move_up())
            self.actions.append(self.move_down())
            self.actions.append(self.move_left())
            self.actions.append(self.move_right())
            self.actions.append(self.turn_up())
            self.actions.append(self.turn_down())
            self.actions.append(self.turn_left())
            self.actions.append(self.turn_right())
            self.actions.append(self.use())

        # Always same orientation, can only move up or down
        if self.avatar_type == "VerticalAvatar":
            self.actions.append(self.move_up())
            self.actions.append(self.move_down())


        self.actions.append(self.nil()) # As last resource, don't do anything
        

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def move_up(self):
        name = "AVATAR_MOVE_UP"
        parameters = [["a", self.avatar_type]]
        
        # can-move indicates that te avatar has the ability to move in that direction
        conditions = ["(can-move-up ?a)", "(orientation-up ?a)"]
        effects = ["(decrease (coordinate_x ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def move_down(self):
        name = "AVATAR_MOVE_DOWN"
        parameters = [["a", self.avatar_type]]

        # can-move indicates that te avatar has the ability to move in that direction
        conditions = ["(can-move-up ?a)", "(orientation-down ?a)"]
        effects = ["(increase (coordinate_x ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def move_left(self):
        name = "AVATAR_MOVE_LEFT"
        parameters = [["a", self.avatar_type]]
        
        # can-move indicates that te avatar has the ability to move in that direction
        conditions = ["(can-move-up ?a)", "(orientation-left ?a)"]
        effects = ["(decrease (coordinate_y ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def move_right(self):
        name = "AVATAR_MOVE_RIGHT"
        parameters = [["a", self.avatar_type]]

        # can-move indicates that te avatar has the ability to move in that direction
        conditions = ["(can-move-up ?a)", "(orientation-right ?a)"]
        effects = ["(increase (coordinate_y ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    # This method should only be called if the avatar can turn
    def turn_up(self):
        name = "AVATAR_TURN_UP"
        parameters = [["a", self.avatar_type]]
        
        # If not (can-change-orientation ?a), the avatar cannot use this action
        conditions = ["(can-change-orientation ?a)","(not (orientation-up ?a))"]

        effect_down = """
                    (when
                        (orientation-down ?a )
                        (not (orientation-down ?a))
                    )"""        
        effect_left = """
                    (when
                        (orientation-left ?a )
                        (not (orientation-left ?a))
                    )"""
        effect_right = """
                    (when
                        (orientation-right ?a )
                        (not (orientation-right ?a))
                    )"""
        effects = [effect_down, effect_right, effect_left, "(orientation-up ?a)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def turn_down(self):
        name = "AVATAR_TURN_DOWN"
        parameters = [["a", self.avatar_type]]

        # If not (can-change-orientation ?a), the avatar cannot use this action
        conditions = ["(can-change-orientation ?a)","(not (orientation-down ?a))"]
        
        effect_up = """
                    (when
                        (orientation-up ?a )
                        (not (orientation-up ?a))
                    )"""
        effect_left = """
                    (when
                        (orientation-left ?a )
                        (not (orientation-left ?a))
                    )"""
        effect_right = """
                    (when
                        (orientation-right ?a )
                        (not (orientation-right ?a))
                    )"""
        effects = [effect_left, effect_right, effect_up, "(orientation-down ?a)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def turn_left(self):
        name = "AVATAR_TURN_LEFT"
        parameters = [["a", self.avatar_type]]      
        
        # If not (can-change-orientation ?a), the avatar cannot use this action
        conditions = ["(can-change-orientation ?a)","(not (orientation-left ?a))"]

        effect_down = """
                    (when
                        (orientation-down ?a )
                        (not (orientation-down ?a))
                    )"""
        effect_up = """
                    (when
                        (orientation-up ?a )
                        (not (orientation-up ?a))
                    )"""
        effect_right = """
                    (when
                        (orientation-right ?a )
                        (not (orientation-right ?a))
                    )"""

        effects = [effect_down, effect_right, effect_up, "(orientation-left ?a)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def turn_right(self):
        name = "AVATAR_TURN_RIGHT"
        parameters = [["a", self.avatar_type]]
        
        # If not (can-change-orientation ?a), the avatar cannot use this action
        conditions = ["(can-change-orientation ?a)","(not (orientation-right ?a))"]

        effect_down = """
                    (when
                        (orientation-down ?a )
                        (not (orientation-down ?a))
                    )"""
        effect_up = """
                    (when
                        (orientation-up ?a )
                        (not (orientation-up ?a))
                    )"""
        effect_left = """
                    (when
                        (orientation-left ?a )
                        (not (orientation-left ?a))
                    )"""
        effects = [effect_down, effect_left, effect_up, "(orientation-right ?a)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    # can-use is a predicate that should not be active in case there is no ammo
    def use(self):
        """ Generates the partner object in front of the avatar

        partner:     Sprite that is generated
        """
        if self.partner == None:
            raise TypeError('Argument "partner" is not defined')

        name = "AVATAR_USE"
        parameters = [["a", self.avatar_type], ["p", self.partner.name]]
        conditions = ["(can-use ?a)"]
        
        # Generate the partner object in a position depending of the orientation of the avatar
        partner_generation = """
                    (when
                        (orientation-up ?a)

                        (and
                            (assign (coordinate_x ?p) (coordinate_x ?a))
                            (assign (coordinate_y ?p) (coordinate_y ?a))
                            (decrease (coordinate_y ?p) 1)						
                        )
                    )

                    (when
                        (orientation-down ?a)

                        (and
                            (assign (coordinate_x ?p) (coordinate_x ?a))
                            (assign (coordinate_y ?p) (coordinate_y ?a))
                            (increase (coordinate_y ?p) 1)						
                        )
                    )

                    (when
                        (orientation-left ?a)

                        (and
                            (assign (coordinate_x ?p) (coordinate_x ?a))
                            (assign (coordinate_y ?p) (coordinate_y ?a))
                            (decrease (coordinate_x ?p) 1)						
                        )
                    )

                    (when
                        (orientation-right ?a)

                        (and
                            (assign (coordinate_x ?p) (coordinate_x ?a))
                            (assign (coordinate_y ?p) (coordinate_y ?a))
                            (increase (coordinate_x ?p) 1)						
                        )
                    )"""
        effects = ["(increase (counter_" + self.partner.name + ") 1)", partner_generation]


        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # Probably will not work
    def nil(self):
        """ Avatar doesn't do anything """
        name = "AVATAR_NIL"
        parameters = [["a", self.avatar_type]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class AvatarPredicates:
    """ Returns different predicates depending of the avatar """
    def __init__(self, avatar_name, avatar_type):
        self.avatar_name = avatar_name
        self.avatar_type = avatar_type

        self.predicates = []
        self.get_predicates()

    def get_predicates(self):
        """ Return a list of predicates depending of the avatar """

        # Can't move but can use object
        if self.avatar_type == "AimedAvatar":
            self.predicates.append("(can-use ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-change-orientation ?a - " + self.avatar_type + ")")

        # This avatar should have ammo
        # Always same orientation, can move horizontally and use object
        if self.avatar_type == "FlakAvatar":
            self.predicates.append("(can-move-left ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-move-right ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-use ?a - " + self.avatar_type + ")")

        # Always same orientation, can only move left or right
        if self.avatar_type == "HorizontalAvatar":
            self.predicates.append("(can-move-left ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-move-right ?a - " + self.avatar_type + ")")

        # Always same orientation, can move in any direction
        if self.avatar_type == "MovingAvatar":
            self.predicates.append("(can-move-up ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-move-down ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-move-left ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-move-right ?a - " + self.avatar_type + ")")

        # ONLY GVGAI
        if self.avatar_type == "OngoingShootAvatar":
            pass

        # ONLY GVGAI
        if self.avatar_type == "OngoingTurningAvatar":
            pass

        # Can move and aim in any direction
        if self.avatar_type == "OrientedAvatar":
            self.predicates.append("(can-move-up ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-move-down ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-move-left ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-move-right ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-change-orientation ?a - " + self.avatar_type + ")")
        
        # Can move and aim in any direction, can use object
        if self.avatar_type == "ShootAvatar":
            self.predicates.append("(can-move-up ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-move-down ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-move-left ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-move-right ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-change-orientation ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-use ?a - " + self.avatar_type + ")")

        # Always same orientation, can only move up or down
        if self.avatar_type == "VerticalAvatar":
            self.predicates.append("(can-move-up ?a - " + self.avatar_type + ")")
            self.predicates.append("(can-move-down ?a - " + self.avatar_type + ")")
