###############################################################################
# predicatesGenerators.py
# Ignacio Vellido Expósito
# 06/09/2019
# 
# Each class produces predicates for a PDDL/HPDL domain
###############################################################################

class AvatarPredicatesGenerator:
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