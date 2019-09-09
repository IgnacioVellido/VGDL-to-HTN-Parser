###############################################################################
# interaction.py
# Ignacio Vellido Expósito
# 09/09/2019
# 
# Multiple classes defining parts of a HPDL domain for interactions
###############################################################################

from hpdl.hpdlTypes import *

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

# If resource is collected, increase +1

class InteractionActions:
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