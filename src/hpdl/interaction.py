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
                       interaction, parameters):

        self.sprite_name  = sprite_name
        self.sprite_type  = sprite_stype
        self.partner_name = partner_name
        self.partner_type = partner_stype    
        self.interaction  = interaction
        self.parameters   = parameters

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
            self.transformTo()
            pass

        # [GVGAI] Transform sprite to one of his childs
        if self.interaction == "transformToRandomChild":
            self.transformToRandomChild()
            pass

        # [GVGAI] Transform all sprites of stype to stype_other in the same position
        if self.interaction == "transformToSingleton":
            self.transformToSingleton()
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

    def addHealthPoints(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_ADDHEALTHPOINTS"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def addHealthPointsToMax(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_ADDHEALTHPOINTSTOMAX"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def align(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_ALIGN"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def attractGaze(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_ATTRACTGAZE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def bounceDirection(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_BOUNCEDIRECTION"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def bounceForward(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_BOUNCEFORWARD"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def changeResource(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_CHANGERESOURCE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def cloneSprite(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_CLONESPRITE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def collectResource(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_COLLECTRESOURCE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [["(assign (last_coordinate_y ?x) (coordinate_x ?x))"],
					["(assign (last_coordinate_y ?x) (coordinate_y ?x))"],
					["(assign (coordinate_x ?x) -1)"],
					["(assign (coordinate_y ?x) -1)"],

					["(decrease (counter_" + self.sprite_type + ") 1)"],
					["(decrease (counter_Resource) 1)"],
					["(decrease (counter_Object) 1)"],

					["(increase (resource_" + self.sprite_type + "diamond ?a) 1)"]]

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def decreaseSpeedToAll(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_INCREASESPEEDTOALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def flipDirection(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_FLIPDIRECTION"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def increaseSpeedToAll(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_INCREASESPEEDTOALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killAll(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_KILLALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killBoth(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_KILLBOTH"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfAlive(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_KILLIFALIVE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfFromAbove(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_KILLIFFROMABOVE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"],
                      ["(= (last_coordinate_y ?y) (- (coordinate_y ?y) 1))"]]
        effects = [["(assign (last_coordinate_y ?a) (coordinate_x ?a))"],
					["(assign (last_coordinate_y ?a) (coordinate_y ?a))"],
					["(assign (coordinate_x ?a) -1)"],
					["(assign (coordinate_y ?a) -1)"],

					["(decrease (counter_" + self.sprite_type + ") 1)"],
					# ["(decrease (counter_ShootAvatar) 1)"], RECORRER LOS PADRES
					# ["(decrease (counter_moving) 1)"],
					["(decrease (counter_Object) 1)"]]

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfHasMore(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_KILLIFHASMORE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfFast(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_KILLIFFAST"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfOtherHasLess(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_KILLIFOTHERHASLESS"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfOtherHasMore(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_KILLIFOTHERHASMORE"
        # + self.third_sprite_type.upper() FIND TYPE IN PARAMETERS OF ACTION
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfSlow(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_KILLIFSLOW"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killSprite(self):
        pass
        
        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_KILLSPRITE"        
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [ ["(assign (last_coordinate_y ?x) (coordinate_x ?x))"]
					["(assign (last_coordinate_y ?x) (coordinate_y ?x))"],
					["(assign (coordinate_x ?x) -1)"],
					["(assign (coordinate_y ?x) -1)"],

					["(decrease (counter_" + self.sprite_type + ") 1)"],
					# ["(decrease (counter_Immovable) 1)"], RECORRER POR TODOS LOS PADRES
					["(decrease (counter_Object) 1)"]]

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def pullWithIt(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_PULLWITHIT"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def removeScore(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_REMOVESCORE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def reverseDirection(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_REVERSEDIRECTION"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def setSpeedToAll(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_SETSPEEDTOALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def spawnBehind(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_SPAWNBEHING"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def spawnIfHasLess(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_SPAWNIFHASLESS"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def spawnIfHasMore(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_SPAWNIFHASMORE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def stepBack(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_STEPBACK"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [["(assign (coordinate_y ?x) (last_coordinate_x ?x))"],
					["(assign (coordinate_y ?x) (last_coordinate_y ?x))"]]

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def subsctractHealthPoints(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_SUBSCTRACTHEALTHPOINTS"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def teleportToExit(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_TELEPORTTOEXIT"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def transformIfCount(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_TRANSFORMIFCOUNT"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def transformTo(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_TRANSFORMTO"
                # + self.third_sprite_type.upper() FIND TYPE IN PARAMETERS OF ACTION
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def transformToRandomChild(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_TRANSFORMTORANDOMCHILD"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def transformToSingleton(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_TRANSFORMTOSINGLETON"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def turnAround(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_TURNAROUND"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def undoAll(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_UNDOALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def updateSpawnType(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_UPDATESPAWNTYPE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def wallBounce(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_WALLBOUNCE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def wallStop(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_WALLSTOP"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def wrapAround(self):
        pass

        name = self.sprite_name.upper() +"_" + self.partner_name.upper() + "_WRAPAROUND"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = []

        return Action(name, parameters, conditions, effects)        