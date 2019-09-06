###############################################################################
# actionsGenerators.py
# Ignacio Vellido Expósito
# 26/08/2019
# 
# Each class produces actions for a PDDL/HPDL domain
###############################################################################

from hpdl.hpdlTypes import Action

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

# RECIEVE partner IN initializer ?

class AvatarActionsGenerator:
    """ Returns different actions depending of the avatar """
    def __init__(self, avatar_name, avatar_type):
        self.avatar_name = avatar_name
        self.avatar_type = avatar_type

    # Podrían juntarse para no repetir código pero lo haría menos legible
    def get_actions(self, partner=None):
        """ Return a list of actions depending of the avatar 
        
        partner:    If ACTION_USE is available for the avatar, 'partner' is the 
                    sprite that is produced
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

        # This avatar should have ammo
        # Always same orientation, can move horizontally and use object
        if self.avatar_type == "FlakAvatar":
            actions.append(self.move_left())
            actions.append(self.move_right())
            # actions.append(self.use(partner))

        # Always same orientation, can only move left or right
        if self.avatar_type == "HorizontalAvatar":
            # actions.append(self.move_left())
            # actions.append(self.move_right())
            pass            

        # Always same orientation, can move in any direction
        if self.avatar_type == "MovingAvatar":
            # actions.append(self.move_up())
            # actions.append(self.move_down())
            # actions.append(self.move_left())
            # actions.append(self.move_right())
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
        
        # Can move and aim in any direction, can use object
        if self.avatar_type == "ShootAvatar":
            actions.append(self.move_up())
            actions.append(self.move_down())
            actions.append(self.move_left())
            actions.append(self.move_right())
            actions.append(self.turn_up())
            actions.append(self.turn_down())
            actions.append(self.turn_left())
            actions.append(self.turn_right())
            # actions.append(self.use(partner))

        # Always same orientation, can only move up or down
        if self.avatar_type == "VerticalAvatar":
            # actions.append(self.move_up())
            # actions.append(self.move_down())
            pass
        
        return actions

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def move_up(self):
        name = "AVATAR_MOVE_UP"
        parameters = [["a", self.avatar_type], ["o", 'Orientation']]
        
        # can-move indicates that te avatar has the ability to move in that direction
        conditions = ["(can-move-up ?a)", "(orientation ?a ?o)", "(or (= ?o none) (= ?o up))"]
                    #   "(or (not (orientation ?a ?)) (and (orientation ?a up) (= (?o up))))"]        
        effects = ["(decrease (coordinate_x ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def move_down(self):
        name = "AVATAR_MOVE_DOWN"
        parameters = [["a", self.avatar_type], ["o", 'Orientation']]
        
        # SOME AVATARS DONT NEED TO BE ORIENTED

        # can-move indicates that te avatar has the ability to move in that direction
        conditions = ["(can-move-down ?a)", "(orientation ?a ?o)", "(or (= ?o none) (= ?o down))"]
                    #   "(or (not (orientation ?a ?)) (and (orientation ?a down) (= (?o down))))"]        
        effects = ["(increase (coordinate_x ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def move_left(self):
        name = "AVATAR_MOVE_LEFT"
        parameters = [["a", self.avatar_type], ["o", 'Orientation']]
        
        # can-move indicates that te avatar has the ability to move in that direction
        conditions = ["(can-move-left ?a)", "(orientation ?a ?o)", "(or (= ?o none) (= ?o left))"]
                    #   "(or (not (orientation ?a ?)) (and (orientation ?a left) (= (?o left))))"]        
        effects = ["(decrease (coordinate_y ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def move_right(self):
        name = "AVATAR_MOVE_RIGHT"
        parameters = [["a", self.avatar_type], ["o", 'Orientation']]

        # can-move indicates that te avatar has the ability to move in that direction
        conditions = ["(can-move-right ?a)", "(orientation ?a ?o)", "(or (= ?o none) (= ?o right))"]
                    #   "(or (not (orientation ?a ?)) (and (orientation ?a right) (= (?o right))))"]        
        effects = ["(increase (coordinate_y ?a) 1)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    # This method should only be called if the avatar can turn
    def turn_up(self):
        name = "AVATAR_TURN_UP"
        parameters = [["a", self.avatar_type], ["o", 'Orientation']]
        
        # If orientation == none, the avatar can change orientation
        conditions = ["(orientation ?a ?o)", "(not (= ?o none))"]  

        effects = ["(not (orientation ?a ?o))", "(orientation ?a up)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def turn_down(self):
        name = "AVATAR_TURN_DOWN"
        parameters = [["a", self.avatar_type], ["o", 'Orientation']]        

        # If orientation == none, the avatar can change orientation
        conditions = ["(orientation ?a ?o)", "(not (= ?o none))"]

        effects = ["(not (orientation ?a ?o))", "(orientation ?a down)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def turn_left(self):
        name = "AVATAR_TURN_LEFT"
        parameters = [["a", self.avatar_type], ["o", 'Orientation']]      
        
        # If orientation == none, the avatar can change orientation
        conditions = ["(orientation ?a ?o)", "(not (= ?o none))"]

        effects = ["(not (orientation ?a ?o))", "(orientation ?a left)"]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    def turn_right(self):
        name = "AVATAR_TURN_RIGHT"
        parameters = [["a", self.avatar_type], ["o", 'Orientation']]      
        
        # If orientation == none, the avatar can change orientation
        conditions = ["(orientation ?a ?o)", "(not (= ?o none))"]

        effects = ["(not (orientation ?a ?o))", "(orientation ?a right)"]

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

def SpriteActionsGenerator():
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
            # actions.append(self.produce(partner))        
            # actions.append(self.move(direction ??))
            pass

        # Follows partner (or avatar ?) object
        if self.sprite_type == "Chaser":    
            # actions.append(self.follow(partner))        
            pass

        # Missile that randomly changes direction
        if self.sprite_type == "ErraticMissile":     
            # actions.append(self.move(direction ??))                   
            # actions.append(self.changeDirection()) - DOESN'T MAKE SENSE TO BE AN ACTION, IT'S RANDOM
            pass

        # Try to make the greatest distance with the partner (or avatar) object
        if self.sprite_type == "Fleeing":       
            # actions.append(self.flee(partner))     
            pass

        # Maybe not needed here
        # Object that dissapear after a moment
        if self.sprite_type == "Flicker":
            # actions.append(self.disappear())
            pass

        # Object that moves constantly in one direction
        if self.sprite_type == "Missile":          
            # actions.append(self.move(direction ??))              
            pass

        # Maybe not needed here
        # Oriented object that dissapear after a moment
        if self.sprite_type == "OrientedFlicker":            
            # actions.append(self.dissapear())
            pass

        # Acts like a Chaser but sometimes it makes a random move
        if self.sprite_type == "RandomAltChaser":  
            # The same actions that Chaser, random moves don't need to be defined
            pass
        
        # Acts like a Bomber but randomly change direction
        if self.sprite_type == "RandomBomber":            
            # The same actions that Bomber, random moves don't need to be defined
            pass

        # Acts like a Missile but randomly change direction
        if self.sprite_type == "RandomMissile":            
            # The same actions that Missile, random moves don't need to be defined
            pass

        # Chooses randomly an action in each iteration
        if self.sprite_type == "RandomNPC":         
            # We can't know wich action will he choose, probably this will be empty  
            # In case we want to add something, we should add each action of the NPC 
            pass

        # Produces objects following a specific ratio
        if self.sprite_type == "SpawnPoint":  
            # actions.append(self.produce(partner))          
            pass

        # Expands in 4 directions if not occupied
        if self.sprite_type == "Spreader":       
            # actions.append(self.expand())     
            pass

        # Missile that if when it collides it change to a random direction
        if self.sprite_type == "Walker":
            # actions.append(self.move(direction ??))
            # If collides stop calculating until we know the new direction
            pass

        # Not clear what it does
        if self.sprite_type == "WalkerJumper":            
            pass

       
        return actions

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def move(self, direction):
        """ Move the object one position in the specified direction """
        pass

        name = self.sprite_name + "_MOVE"
        parameters = [["s", self.sprite_type]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def expand(self):
        """ Expand all objects in the 4 directions if unoccupied """ 
        # If no other object in that position...
        pass

        name = self.sprite_name + "_EXPAND"
        parameters = [["s", self.sprite_type]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        
    
    # -------------------------------------------------------------------------

    def produce(self, partner):
        """ Generate an object - IN WICH POSITION ?? """
        pass

        name = self.sprite_name + "_PRODUCE"
        parameters = [["s", self.sprite_type], ["p", partner.name]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def dissapear(self):
        """ Eliminates the object """
        pass

        name = self.sprite_name + "_DISSAPEAR"
        parameters = [["s", self.sprite_type]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def chase(self, partner):
        """ Choose the movement that moves toward the closest sprite of the 
        partner type """
        pass

        name = self.sprite_name + "_CHASE"
        parameters = [["s", self.sprite_type], ["p", partner.name]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def flee(self, partner):
        """ Choose the movement that moves away the closest sprite of the
        partner type """        
        pass

        name = self.sprite_name + "_FLEE"
        parameters = [["s", self.sprite_type], ["p", partner.name]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        


###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

# If resource is collected, increase +1

class InteractionActionsGenerator():
    """ Returns an action for each interaction """
    def __init__(self, sprite_name, sprite_stype, 
                       partner_name, partner_stype,
                       interaction):

        self.interaction  = interaction
        self.sprite_name = sprite_name
        self.sprite_type = sprite_stype
        self.partner_name = partner_name
        self.partner_type = partner_stype    

    def get_actions(self):
        """ Return a list of actions depending of the interaction """
        actions = []

        # [GVGAI] Adds a certain quantity of health points
        if self.interaction == "addHealthPoints":
            self.addHealthPoints()
            pass    

        # [GVGAI] Puts health points to max
        if self.interaction == "addHealthPointsToMax":
            self.addHealthPointsToMax()
            pass    

        # [GVGAI] Changes position and orientation of sprite to partner
        if self.interaction == "align":
            self.align()
            pass    

        # Randomly changesdirection of partner
        if self.interaction == "attractGaze":
            self.attractGaze()
            pass    

        # Not sure what it does, seems like the center of the object decides the direction
        if self.interaction == "bounceDirection":
            self.bounceDirection()
            pass    

        # Sprite tries to move in the opposite direction of partner
        if self.interaction == "bounceForward":
            self.bounceForward()
            pass    

        # Change resource (sprite) in the object (partner) to a given
        if self.interaction == "changeResource":
            self.changeResource()
            pass

        # Creates a copy
        if self.interaction == "cloneSprite":
            self.cloneSprite()
            pass

        # Increment resource (sprite) in the object (partner)
        if self.interaction == "collectResource":
            self.collectResource()
            pass    

        # [GVGAI] Decrease speed of all objects of the type of the sprite
        if self.interaction == "decreaseSpeedToAll":
            self.decreaseSpeedToAll()
            pass    

        # Changes to a random orientation
        if self.interaction == "flipDirection":
            self.flipDirection()
            pass

        # [GVGAI] Increase speed of all objects of the sprite type
        if self.interaction == "increaseSpeedToAll":
            self.increaseSpeedToAll()
            pass    

        # [GVGAI] Kill all sprite of the same type
        if self.interaction == "killAll":
            self.killAll()
            pass        

        # Sprite and partner dies
        if self.interaction == "killBoth":
            self.killBoth()
            pass

        # Kill sprite if partner is not destroyed by the collision
        if self.interaction == "killIfAlive":
            self.killIfAlive()
            pass    

        # Kill sprite if partner is above him
        if self.interaction == "killIfFromAbove":
            self.killIfFromAbove()
            pass        

        # If sprite has more resource than parameter (limit), kill it
        if self.interaction == "killIfHasMore":
            self.killIfHasMore()
            pass    

        # Not found in the GVGAI files
        # If sprite has less resource than parameter (limit), kill it
        # if self.interaction == "killIfHasLess":
            # pass    

        # Kill sprite if speed is higher than the given
        if self.interaction == "killIfFast":
            self.killIfFast()
            pass    

        # If partner has less resource than parameter (limit), kill sprite
        if self.interaction == "killIfOtherHasLess":
            self.killIfOtherHasLess()
            pass

        # If partner has more resource than parameter (limit), kill sprite
        if self.interaction == "killIfOtherHasMore":
            self.killIfOtherHasMore()
            pass

        # Kill sprite if speed is lower than the given
        if self.interaction == "killIfSlow":
            self.killIfSlow()
            pass    

        # Sprite dies
        if self.interaction == "killSprite":
            self.killSprite()
            pass

        # Movement of partner is added to sprite (same quantity and direction)
        if self.interaction == "pullWithIt":
            self.pullWithIt()
            pass

        # [GVGAI] Changes score of the avatar
        if self.interaction == "removeScore":
            self.removeScore()
            pass    

        # Changes orientation 180º
        if self.interaction == "reverseDirection":
            self.reverseDirection()
            pass

        # [GVGAI] Asigns a specific speed to the sprite
        if self.interaction == "setSpeedToAll":
            self.setSpeedToAll()
            pass    

        # Creates sprite behind partner
        if self.interaction == "spawnBehind":
            self.spawnBehind()
            pass    

        # If sprite has less resource than parameter (limit), create new sprite
        if self.interaction == "spawnIfHasLess":
            self.spawnIfHasLess()
            pass

        # If sprite has more resource than parameter (limit), create new sprite
        if self.interaction == "spawnIfHasMore":
            self.spawnIfHasMore()
            pass

        # Undo last movement
        if self.interaction == "stepBack":
            self.stepBack()
            pass

        # [GVGAI] Decrease a certain quantity of health points
        if self.interaction == "substractHealthPoints":
            self.subsctractHealthPoints()
            pass    

        # Move sprite to partner position (must be a Portal, if not, destroy sprite)
        if self.interaction == "teleportToExit":
            self.teleportToExit()
            pass    

        # [GVGAI] Changes sprite to stype if there are a certain quantity (stypeCount)
        if self.interaction == "transformIfCount":
            self.transformIfCounts()
            pass

        # Seems like it creates a new copy of sprite
        if self.interaction == "transformTo":
            self.tranformTo
            pass

        # [GVGAI] Transform sprite to one of his childs
        if self.interaction == "transformToRandomChild":
            self.tranformToRandomChild()
            pass

        # [GVGAI] Transform all sprites of stype to stype_other in the same position
        if self.interaction == "transformToSingleton":
            self.tranformToSingleton()
            pass

        # Not sure what it does, in VGDL seems to call reverseDirection
        if self.interaction == "turnAround":
            self.turnAround()
            pass

        # Undo movement of every object in the game
        if self.interaction == "undoAll":
            self.undoAll()
            pass

        # [GVGAI] Changes the "spawn type" to SpawnPoint
        if self.interaction == "updateSpawnType":
            self.updateSpawnType()
            pass    

        # Bounce in a perpendicular direction from the wall
        if self.interaction == "wallBounce":
            self.wallBounce()
            pass        

        # Stops sprite in front of wall
        if self.interaction == "wallStop":
            self.wallStop()
            pass

        # Move sprite at the end of the screen in the orientation of sprite
        if self.interaction == "wrapAround":
            self.wrapAround()
            pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def addHealthPoints():
        pass

    # -------------------------------------------------------------------------

    def addHealthPointsToMax():
        pass

    # -------------------------------------------------------------------------

    def align():
        pass

    # -------------------------------------------------------------------------

    def attractGaze():
        pass

    # -------------------------------------------------------------------------

    def bounceDirection():
        pass

    # -------------------------------------------------------------------------

    def bounceForward():
        pass

    # -------------------------------------------------------------------------

    def changeResource():
        pass

    # -------------------------------------------------------------------------

    def cloneSprite():
        pass

    # -------------------------------------------------------------------------

    def collectResource():
        pass

    # -------------------------------------------------------------------------

    def decreaseSpeedToAll():
        pass

    # -------------------------------------------------------------------------

    def flipDirection():
        pass

    # -------------------------------------------------------------------------

    def increaseSpeedToAll():
        pass

    # -------------------------------------------------------------------------

    def killAll():
        pass

    # -------------------------------------------------------------------------

    def killBoth():
        pass

    # -------------------------------------------------------------------------

    def killIfAlive():
        pass

    # -------------------------------------------------------------------------

    def killIfFromAbove():
        pass

    # -------------------------------------------------------------------------

    def killIfHasMore():
        pass

    # -------------------------------------------------------------------------

    def killIfFast():
        pass

    # -------------------------------------------------------------------------

    def killIfOtherHasLess():
        pass

    # -------------------------------------------------------------------------

    def killIfOtherHasMore():
        pass

    # -------------------------------------------------------------------------

    def killIfSlow():
        pass

    # -------------------------------------------------------------------------

    def killSprite():
        pass

    # -------------------------------------------------------------------------

    def pullWithIt():
        pass

    # -------------------------------------------------------------------------

    def removeScore():
        pass

    # -------------------------------------------------------------------------

    def reverseDirection():
        pass

    # -------------------------------------------------------------------------

    def setSpeedToAll():
        pass

    # -------------------------------------------------------------------------

    def spawnBehind():
        pass

    # -------------------------------------------------------------------------

    def spawnIfHasLess():
        pass

    # -------------------------------------------------------------------------

    def spawnIfHasMore():
        pass

    # -------------------------------------------------------------------------

    def stepBack():
        pass

    # -------------------------------------------------------------------------

    def subsctractHealthPoints():
        pass

    # -------------------------------------------------------------------------

    def teleportToExit():
        pass

    # -------------------------------------------------------------------------

    def transformIfCount():
        pass

    # -------------------------------------------------------------------------

    def transformTo():
        pass

    # -------------------------------------------------------------------------

    def tranformToRandomChild():
        pass

    # -------------------------------------------------------------------------

    def tranformToSingleton():
        pass

    # -------------------------------------------------------------------------

    def turnAround():
        pass

    # -------------------------------------------------------------------------

    def undoAll():
        pass

    # -------------------------------------------------------------------------

    def updateSpawnType():
        pass

    # -------------------------------------------------------------------------

    def wallBounce():
        pass

    # -------------------------------------------------------------------------

    def wallStop():
        pass

    # -------------------------------------------------------------------------

    def wrapAround():
        pass