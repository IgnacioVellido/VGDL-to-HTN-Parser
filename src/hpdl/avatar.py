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
            # self.actions.append(self.turn_up())
            # self.actions.append(self.turn_down())
            # self.actions.append(self.turn_left())
            # self.actions.append(self.turn_right())
            # self.actions.append(self.use())
            pass

        # This avatar should have ammo
        # Always same orientation, can move horizontally and use object
        if self.avatar_type == "FlakAvatar":
            self.actions.append(self.move_left())
            self.actions.append(self.move_right())
            self.actions.append(self.use())

        # Always same orientation, can only move left or right
        if self.avatar_type == "HorizontalAvatar":
            # self.actions.append(self.move_left())
            # self.actions.append(self.move_right())
            pass            

        # Always same orientation, can move in any direction
        if self.avatar_type == "MovingAvatar":
            # self.actions.append(self.move_up())
            # self.actions.append(self.move_down())
            # self.actions.append(self.move_left())
            # self.actions.append(self.move_right())
            pass       

        # ONLY GVGAI
        if self.avatar_type == "OngoingShootAvatar":
            pass

        # ONLY GVGAI
        if self.avatar_type == "OngoingTurningAvatar":
            pass

        # Can move and aim in any direction
        if self.avatar_type == "OrientedAvatar":
            # self.actions.append(self.move_up())
            # self.actions.append(self.move_down())
            # self.actions.append(self.move_left())
            # self.actions.append(self.move_right())
            # self.actions.append(self.turn_up())
            # self.actions.append(self.turn_down())
            # self.actions.append(self.turn_left())
            # self.actions.append(self.turn_right())
            pass
        
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
            # self.actions.append(self.move_up())
            # self.actions.append(self.move_down())
            pass


        self.actions.append(self.nil()) # As last resource, don't do anything
        

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def move_up(self):
        name = "AVATAR_MOVE_UP"
        parameters = [["a", self.avatar_type], ["o", 'Orientation']]
        
        # can-move indicates that te avatar has the ability to move in that direction
        conditions = ["(can-move-up ?a)", "(orientation ?a ?o)", "(= ?o up)"]        
        effects = ["(decrease (coordinate_x ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def move_down(self):
        name = "AVATAR_MOVE_DOWN"
        parameters = [["a", self.avatar_type], ["o", 'Orientation']]        

        # can-move indicates that te avatar has the ability to move in that direction
        conditions = ["(can-move-down ?a)", "(orientation ?a ?o)", "(= ?o down)"]
        effects = ["(increase (coordinate_x ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def move_left(self):
        name = "AVATAR_MOVE_LEFT"
        parameters = [["a", self.avatar_type], ["o", 'Orientation']]
        
        # can-move indicates that te avatar has the ability to move in that direction
        conditions = ["(can-move-left ?a)", "(orientation ?a ?o)", "(= ?o left)"]
        effects = ["(decrease (coordinate_y ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def move_right(self):
        name = "AVATAR_MOVE_RIGHT"
        parameters = [["a", self.avatar_type], ["o", 'Orientation']]

        # can-move indicates that te avatar has the ability to move in that direction
        conditions = ["(can-move-right ?a)", "(orientation ?a ?o)", "(= ?o right)"]
        effects = ["(increase (coordinate_y ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    # This method should only be called if the avatar can turn
    def turn_up(self):
        name = "AVATAR_TURN_UP"
        parameters = [["a", self.avatar_type], ["o", 'Orientation']]
        
        # If not (can-change-orientation ?a), the avatar cannot use this action
        conditions = ["(can-change-orientation ?a)","(orientation ?a ?o)"]

        effects = ["(not (orientation ?a ?o))", "(orientation ?a up)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def turn_down(self):
        name = "AVATAR_TURN_DOWN"
        parameters = [["a", self.avatar_type], ["o", 'Orientation']]        

        # If not (can-change-orientation ?a), the avatar cannot use this action
        conditions = ["(can-change-orientation ?a)","(orientation ?a ?o)"]

        effects = ["(not (orientation ?a ?o))", "(orientation ?a down)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def turn_left(self):
        name = "AVATAR_TURN_LEFT"
        parameters = [["a", self.avatar_type], ["o", 'Orientation']]      
        
        # If not (can-change-orientation ?a), the avatar cannot use this action
        conditions = ["(can-change-orientation ?a)","(orientation ?a ?o)"]

        effects = ["(not (orientation ?a ?o))", "(orientation ?a left)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def turn_right(self):
        name = "AVATAR_TURN_RIGHT"
        parameters = [["a", self.avatar_type], ["o", 'Orientation']]      
        
        # If not (can-change-orientation ?a), the avatar cannot use this action
        conditions = ["(can-change-orientation ?a)","(orientation ?a ?o)"]

        effects = ["(not (orientation ?a ?o))", "(orientation ?a right)"]

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
        effects = ["(increase (counter_" + self.partner.name + ") 1)"]

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


class AvatarTasks:
    """ Returns a task depending of the avatar """
    def __init__(self, avatar_name, avatar_type, partner):
        self.avatar_name = avatar_name
        self.avatar_type = avatar_type

        self.tasks = []
        self.get_tasks()

    def get_tasks(self):
        pass

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class AvatarPredicates:
    """ Returns different predicates depending of the avatar """
    def __init__(self, avatar_name, avatar_type):
        self.avatar_name = avatar_name
        self.avatar_type = avatar_type

    def get_predicates(self, partner=None):
        """ Return a list of predicates depending of the avatar """
        predicates = []

        # Although some avatars can change orientation, this predicate is needed for the actions
        predicates.append("(orientation ?a - " + self.avatar_type 
                            + " ?o - Orientation)") 

        # Can't move but can use object
        if self.avatar_type == "AimedAvatar":
            predicates.append("(can-use ?a - " + self.avatar_type + ")")
            predicates.append("(can-change-orientation ?a - " + self.avatar_type + ")")

        # This avatar should have ammo
        # Always same orientation, can move horizontally and use object
        if self.avatar_type == "FlakAvatar":
            predicates.append("(can-move-left ?a - " + self.avatar_type + ")")
            predicates.append("(can-move-right ?a - " + self.avatar_type + ")")
            predicates.append("(can-use ?a - " + self.avatar_type + ")")

        # Always same orientation, can only move left or right
        if self.avatar_type == "HorizontalAvatar":
            predicates.append("(can-move-left ?a - " + self.avatar_type + ")")
            predicates.append("(can-move-right ?a - " + self.avatar_type + ")")

        # Always same orientation, can move in any direction
        if self.avatar_type == "MovingAvatar":
            predicates.append("(can-move-up ?a - " + self.avatar_type + ")")
            predicates.append("(can-move-down ?a - " + self.avatar_type + ")")
            predicates.append("(can-move-left ?a - " + self.avatar_type + ")")
            predicates.append("(can-move-right ?a - " + self.avatar_type + ")")

        # ONLY GVGAI
        if self.avatar_type == "OngoingShootAvatar":
            pass

        # ONLY GVGAI
        if self.avatar_type == "OngoingTurningAvatar":
            pass

        # Can move and aim in any direction
        if self.avatar_type == "OrientedAvatar":
            predicates.append("(can-move-up ?a - " + self.avatar_type + ")")
            predicates.append("(can-move-down ?a - " + self.avatar_type + ")")
            predicates.append("(can-move-left ?a - " + self.avatar_type + ")")
            predicates.append("(can-move-right ?a - " + self.avatar_type + ")")
            predicates.append("(can-change-orientation ?a - " + self.avatar_type + ")")
        
        # Can move and aim in any direction, can use object
        if self.avatar_type == "ShootAvatar":
            predicates.append("(can-move-up ?a - " + self.avatar_type + ")")
            predicates.append("(can-move-down ?a - " + self.avatar_type + ")")
            predicates.append("(can-move-left ?a - " + self.avatar_type + ")")
            predicates.append("(can-move-right ?a - " + self.avatar_type + ")")
            predicates.append("(can-change-orientation ?a - " + self.avatar_type + ")")
            predicates.append("(can-use ?a - " + self.avatar_type + ")")

        # Always same orientation, can only move up or down
        if self.avatar_type == "VerticalAvatar":
            predicates.append("(can-move-up ?a - " + self.avatar_type + ")")
            predicates.append("(can-move-down ?a - " + self.avatar_type + ")")
        
        return predicates

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class AvatarHPDL:
    def __init__(self, avatar_name, avatar_type, partner=None):
        self.avatar_name = avatar_name
        self.avatar_type = avatar_type
        self.patner      = partner

        self.actions    = AvatarActions(avatar_name, avatar_type, partner).actions
        self.methods    = []
        self.get_methods()
        # self.methods    = AvatarMethods(avatar_name, avatar_type, partner).methods
        # self.tasks      = AvatarTasks(avatar_name, avatar_type, partner).tasks
        # self.predicates = AvatarPredicates(avatar_name, avatar_type).predicates

    def get_methods(self):
        for action in self.actions:
            name = action.name.lower()
            preconditions = []

            # Getting the parameters (only the name, not the type)
            parameters = ""
            for p in action.parameters:
                parameters += " ?" + p[0]

            m_action = "(" + action.name + parameters + ")"

            m = Method(name, preconditions, [m_action])

            self.methods.append(m)