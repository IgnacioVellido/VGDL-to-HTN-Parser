###############################################################################
# actionsGenerators.py
# Ignacio Vellido Expósito
# 26/08/2019
# 
# Each class produces actions in a HPDL domain
###############################################################################

class AvatarActionsGenerator:
    def __init__(avatar_name, avatar_type):
        self.avatar_name = avatar_name
        self.avatar_type = avatar_type
    
    def get_actions():
        """ Return a list of actions depending of the avatar """
        actions = []

        if self.avatar_type == "FlakAvatar":
            # These avatar should have ammo
            actions.append(self.move_up()) 
            actions.append(self.move_down())
            actions.append(self.move_left())
            actions.append(self.move_right())
            actions.append(self.move_use())

        return actions

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def move_up():
        name = "AVATAR_UP"
        parameters = [[self.avatar_name, self.avatar_type]]
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------