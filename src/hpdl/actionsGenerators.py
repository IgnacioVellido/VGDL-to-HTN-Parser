###############################################################################
# actionsGenerators.py
# Ignacio Vellido Expósito
# 26/08/2019
# 
# Each class produces actions in a HPDL domain
###############################################################################

from hpdl.hpdlTypes import *

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class AvatarActionsGenerator:
    """ Returns different actions depending of the avatar """
    def __init__(self, avatar_name, avatar_type):
        self.avatar_name = avatar_name
        self.avatar_type = avatar_type

    # Podrían juntarse para no repetir código pero lo haría menos legible
    def get_actions(self, partner=None):
        """ Return a list of actions depending of the avatar 
        
        partner:    If USE is available, sprite that is produced
        """
        actions = []
        actions.append(self.nil()) # Don't do anything

        # Can't move but can use object
        if self.avatar_type == "AimedAvatar":
            # actions.append(self.turn_up())
            # actions.append(self.turn_down())
            # actions.append(self.turn_left())
            # actions.append(self.turn_right())
            # actions.append(self.use(partner))
            pass

        # Remove, not information found
        if self.avatar_type == "BirdAvatar":
            pass

        # Remove, not information found
        if self.avatar_type == "CarAvatar":
            pass

        # This avatar should have ammo
        # Always same orientation, can move horizontally and use object
        if self.avatar_type == "FlakAvatar":
            actions.append(self.move_left())
            actions.append(self.move_right())
            actions.append(self.use(partner))

        # Always same orientation, can only move left or right
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

        # Always same orientation, can move in any direction
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

        # Can move and aim in any direction
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
        
        # Can move and aim in any direction, can use object
        if self.avatar_type == "ShootAvatar":
            # actions.append(self.move_up())
            # actions.append(self.move_down())
            # actions.append(self.move_left())
            # actions.append(self.move_right())
            # actions.append(self.turn_up())
            # actions.append(self.turn_down())
            # actions.append(self.turn_left())
            # actions.append(self.turn_right())
            # actions.append(self.use(partner))
            pass

        # Remove, not information found
        if self.avatar_type == "ShootOnlyAvatar":
            pass

        # Remove, not information found
        if self.avatar_type == "SpaceshipAvatar":
            pass    

        # Always same orientation, can only move up or down
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
    # can-use is a predicate that should not be active in case there is no ammo
    def use(self, partner):
        """ ???


        partner:     Sprite that is generated
        """
        if partner == None:
            raise TypeError('Argument "partner" is not defined')

        name = "AVATAR_USE"
        parameters = [["a", self.avatar_type], ["p", partner.name]]
        conditions = ["(can-use ?a ?p)"]

        # ?????????????
        effects = []

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

def SpriteActionGenerator():
    """ Return actions depending of the sprite (not including avatars) 
    
    These actions define the movements of the sprite not (directly) related with 
    interactions
    """

    def __init__(self, sprite_name, sprite_type):
        self.sprite_name = sprite_name
        self.sprite_type = sprite_type

    # -------------------------------------------------------------------------

    def get_actions(self):
        actions = []

        # Not clear what it does
        # Missile that produces object at a specific ratio
        if self.sprite_type == "Bomber":            
            pass

        # Follows partner (or avatar ?) object
        if self.sprite_type == "Chaser":            
            pass

        # Missile that randomly changes direction
        if self.sprite_type == "ErraticMissile":            
            pass

        # Try to make the greatest distance with the partner (or avatar) object
        if self.sprite_type == "Fleeing":            
            pass

        # Maybe not needed here
        # Object that dissapear after a moment
        if self.sprite_type == "Flicker":
            # actions.append(self.expand())
            pass

        # Object that moves constantly in one direction
        if self.sprite_type == "Missile":            
            pass

        # Remove, no information found
        if self.sprite_type == "PathAltChaser":            
            pass

        # Remove, no information found
        if self.sprite_type == "PathChaser":            
            pass

        # Oriented object that dissapear after a moment
        if self.sprite_type == "OrientedFlicker":            
            # actions.append(self.expand())
            pass

        # Acts like a Chaser but sometimes it makes a random move
        if self.sprite_type == "RandomAltChaser":            
            pass
        
        # Acts like a Bomber but randomly change direction
        if self.sprite_type == "RandomBomber":            
            pass

        # Acts like a Missile but randomly change direction
        if self.sprite_type == "RandomMissile":            
            pass

        # Chooses randomly an action in each iteration
        if self.sprite_type == "RandomNPC":            
            pass

        # Remove, no information found
        if self.sprite_type == "RandomPathAltChaser":            
            pass

        # Produces objects following a specific ratio
        if self.sprite_type == "SpawnPoint":            
            pass

        # Expands in 4 directions if not occupied
        if self.sprite_type == "Spreader":            
            pass

        # Missile that if when it collides it change to a random direction
        if self.sprite_type == "Walker":            
            pass

        # Not clear what it does
        if self.sprite_type == "WalkerJumper":            
            pass

       
        return actions

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------