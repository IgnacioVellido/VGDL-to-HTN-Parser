###############################################################################
# actionsGenerators.py
# Ignacio Vellido Expósito
# 26/08/2019
# 
# Each class produces actions in a HPDL domain
###############################################################################

from hpdl.hpdlTypes import *

class AvatarActionsGenerator:
    def __init__(self, avatar_name, avatar_type):
        self.avatar_name = avatar_name
        self.avatar_type = avatar_type
    
    # ACTION_USE

    # Podrían juntarse para no repetir código pero lo haría menos legible
    def get_actions(self):
        """ Return a list of actions depending of the avatar """
        actions = []
        actions.append(self.nil()) # Don't do anything

        if self.avatar_type == "AimedAvatar":
            # actions.append(self.turn_up())
            # actions.append(self.turn_down())
            # actions.append(self.turn_left())
            # actions.append(self.turn_right())
            # actions.append(self.use())
            pass

        # Remove, not information found
        if self.avatar_type == "BirdAvatar":
            pass

        # Remove, not information found
        if self.avatar_type == "CarAvatar":
            pass

        # This avatar should have ammo
        if self.avatar_type == "FlakAvatar":
            actions.append(self.move_left())
            # actions.append(self.move_right())
            # actions.append(self.use())

        if self.avatar_type == "HorizontalAvatar":
            # actions.append(self.move_left())
            # actions.append(self.move_right())
            pass
            
        # Remove, not information found
        if self.avatar_type == "LanderAvatar":
            pass

        # Remove, is not an avatar. ONLY GVGAI
        if self.avatar_type == "MissileAvatar":
            pass

        if self.avatar_type == "MovingAvatar":
            # actions.append(self.move_up())
            # actions.append(self.move_down())
            # actions.append(self.move_left())
            # actions.append(self.move_right())
            pass

        # Remove, not information found
        if self.avatar_type == "NullAvatar":
            pass       

        # ONLY GVGAI
        if self.avatar_type == "OngoingShootAvatar":
            pass

        # ONLY GVGAI
        if self.avatar_type == "OngoingTurningAvatar":
            pass

        if self.avatar_type == "OrientedAvatar":
            # actions.append(self.move_up())
            # actions.append(self.move_down())
            # actions.append(self.move_left())
            # actions.append(self.move_right())
            # actions.append(self.turn_up())
            # actions.append(self.turn_down())
            # actions.append(self.turn_left())
            # actions.append(self.turn_right())
            pass

        # Remove, not information found
        if self.avatar_type == "PlatformerAvatar":
            pass
        
        if self.avatar_type == "ShootAvatar":
            # actions.append(self.move_up())
            # actions.append(self.move_down())
            # actions.append(self.move_left())
            # actions.append(self.move_right())
            # actions.append(self.turn_up())
            # actions.append(self.turn_down())
            # actions.append(self.turn_left())
            # actions.append(self.turn_right())
            # actions.append(self.use())
            pass

        # Remove, not information found
        if self.avatar_type == "ShootOnlyAvatar":
            pass

        # Remove, not information found
        if self.avatar_type == "SpaceshipAvatar":
            pass    

        if self.avatar_type == "VerticalAvatar":
            # actions.append(self.move_up())
            # actions.append(self.move_down())
            pass

        # Remove, not information found
        if self.avatar_type == "WizardAvatar":
            pass
        
        return actions

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def move_up(self):
        name = "AVATAR_MOVE_UP"
        parameters = [["a", self.avatar_type]]        
        conditions = ["(can-move-up ?a)"]
        effects = ["(decrease (coordinate_x ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def move_down(self):
        name = "AVATAR_MOVE_DOWN"
        parameters = [["a", self.avatar_type]]        
        conditions = ["(can-move-down ?a)"]
        effects = ["(increase (coordinate_x ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def move_left(self):
        name = "AVATAR_MOVE_LEFT"
        parameters = [["a", self.avatar_type]]        
        conditions = ["(can-move-left ?a)"]
        effects = ["(decrease (coordinate_y ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def move_right(self):
        name = "AVATAR_MOVE_RIGHT"
        parameters = [["a", self.avatar_type]]        
        conditions = ["(can-move-right ?a)"]
        effects = ["(increase (coordinate_y ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    # Probably will not work
    def nil(self):
        name = "AVATAR_NIL"
        parameters = [["a", self.avatar_type]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        