###############################################################################
# methodsGenerators.py
# Ignacio Vellido Expósito
# 05/09/2019
# 
# Each class produces methods for a HPDL domain
###############################################################################

from hpdl.hpdlTypes import Method

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class AvatarMethodsGenerator:
    """ Returns different methods depending of the avatar """
    def __init__(self, avatar_name, avatar_type):
        self.avatar_name = avatar_name
        self.avatar_type = avatar_type

    def get_methods(self, partner=None):
        """ Return a list of methods depending of the avatar 
        
        partner:    If ACTION_USE is available for the avatar, 'partner' is the 
                    sprite that is produced
        """
        methods = []
        methods.append(self.nil()) # Don't do anything

        # Can't move but can use object
        if self.avatar_type == "AimedAvatar":
            # methods.append(self.turn_up())
            # methods.append(self.turn_down())
            # methods.append(self.turn_left())
            # methods.append(self.turn_right())
            # methods.append(self.use(partner))
            pass

        # This avatar should have ammo
        # Always same orientation, can move horizontally and use object
        if self.avatar_type == "FlakAvatar":
            methods.append(self.move_left())
            methods.append(self.move_right())
            methods.append(self.use(partner))

        # Always same orientation, can only move left or right
        if self.avatar_type == "HorizontalAvatar":
            # methods.append(self.move_left())
            # methods.append(self.move_right())
            pass            

        # Always same orientation, can move in any direction
        if self.avatar_type == "MovingAvatar":
            # methods.append(self.move_up())
            # methods.append(self.move_down())
            # methods.append(self.move_left())
            # methods.append(self.move_right())
            pass       

        # ONLY GVGAI
        if self.avatar_type == "OngoingShootAvatar":
            pass

        # ONLY GVGAI
        if self.avatar_type == "OngoingTurningAvatar":
            pass

        # Can move and aim in any direction
        if self.avatar_type == "OrientedAvatar":
            # methods.append(self.move_up())
            # methods.append(self.move_down())
            # methods.append(self.move_left())
            # methods.append(self.move_right())
            # methods.append(self.turn_up())
            # methods.append(self.turn_down())
            # methods.append(self.turn_left())
            # methods.append(self.turn_right())
            pass
        
        # Can move and aim in any direction, can use object
        if self.avatar_type == "ShootAvatar":
            methods.append(self.move_up())
            methods.append(self.move_down())
            methods.append(self.move_left())
            methods.append(self.move_right())
            methods.append(self.turn_up())
            methods.append(self.turn_down())
            methods.append(self.turn_left())
            methods.append(self.turn_right())
            # methods.append(self.use(partner))

        # Always same orientation, can only move up or down
        if self.avatar_type == "VerticalAvatar":
            # methods.append(self.move_up())
            # methods.append(self.move_down())
            pass
        
        return methods


        # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def move_up(self):
        name = "move_up"
        preconditions = []
        actions = ["(AVATAR_MOVE_UP ?a ?o)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    def move_down(self):
        name = "move_down"
        preconditions = []
        actions = ["(AVATAR_MOVE_DOWN ?a ?o)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    def move_left(self):
        name = "move_left"
        preconditions = []
        actions = ["(AVATAR_MOVE_LEFT ?a ?o)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    def move_right(self):
        name = "move_right"
        preconditions = []
        actions = ["(AVATAR_MOVE_RIGHT ?a ?o)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    # This method should only be called if the avatar can turn
    def turn_up(self):
        name = "turn_up"
        preconditions = []
        actions = ["(AVATAR_TURN_UP ?a ?o)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    def turn_down(self):
        name = "turn_down"
        preconditions = []
        actions = ["(AVATAR_TURN_DOWN ?a ?o)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    def turn_left(self):
        name = "turn_left"
        preconditions = []
        actions = ["(AVATAR_TURN_LEFT ?a ?o)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    def turn_right(self):
        name = "turn_right"
        preconditions = []
        actions = ["(AVATAR_TURN_RIGHT ?a ?o)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    # Probably will not work
    # can-use is a predicate that should not be active in case there is no ammo
    def use(self, partner):
        """ UNFINISHED """
        name = "use"
        preconditions = []
        actions = ["(AVATAR_USE ?a ?partner)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    # Probably will not work
    def nil(self):
        name = "nil"
        preconditions = []
        actions = ["(AVATAR_NIL ?a)"]    

        return Method(name, preconditions, actions)


###############################################################################
# -----------------------------------------------------------------------------
###############################################################################
