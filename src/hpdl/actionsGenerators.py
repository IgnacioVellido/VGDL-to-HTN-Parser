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
    
    def get_actions(self):
        """ Return a list of actions depending of the avatar """
        actions = []

        if self.avatar_type == "FlakAvatar":
            # This avatar should have ammo)
            actions.append(self.move_left())
            # actions.append(self.move_right())
            # actions.append(self.move_use())
            # actions.append(self.move_nil()) # Don't do anything

        return actions

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def move_left(self):
        name = "AVATAR_MOVE_LEFT"
        parameters = [["a", self.avatar_type]]        
        conditions = ["(can-move-left ?a)"]
        effects = ["(decrease (coordinate_y ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------