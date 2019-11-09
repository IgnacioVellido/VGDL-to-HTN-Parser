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

class InteractionHPDL:
    """ Class that encapsulate the generation of HPDL domain structures 
    for interactions """
    def __init__(self, interaction_type, 
                 sprite_name, sprite_stype, 
                 partner_name, partner_stype,
                 parameters):
        """ Constructor:
        TO DO: PARAMETERS
        """
        self.actions  = InteractionActions(interaction_type, 
                                           sprite_name, sprite_stype, 
                                           partner_name, partner_stype,
                                           parameters).get_actions()
        self.methods  = InteractionMethods(interaction_type, 
                                           sprite_name, sprite_stype, 
                                           partner_name, partner_stype,
                                           parameters).get_methods()
        self.task     = InteractionTasks(methods).get_tasks()
        # self.predicates =

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class InteractionTasks:
    """ Creates the tasks for checking interactions """
    def __init__(self, actions):
        self.actions = actions

    def get_tasks(self):
        pass
 
###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class InteractionMethods:
    """ Returns a method depending of the interaction """
    def __init__(self, sprite_name, sprite_stype, 
                       partner_name, partner_stype,
                       interaction, parameters):

        self.sprite_name  = sprite_name
        self.sprite_type  = sprite_stype
        self.partner_name = partner_name
        self.partner_type = partner_stype    
        self.type         = interaction
        self.parameters   = parameters

    def get_methods(self):
        """ Return a list of methods depending of the interaction """
        actions = []

        # [GVGAI] Adds a certain quantity of health points
        if self.type == "addHealthPoints":
            self.addHealthPoints()
            pass    

        # [GVGAI] Puts health points to max
        if self.type == "addHealthPointsToMax":
            self.addHealthPointsToMax()
            pass    

        # [GVGAI] Changes position and orientation of sprite to partner
        if self.type == "align":
            self.align()
            pass    

        # Randomly changesdirection of partner
        if self.type == "attractGaze":
            self.attractGaze()
            pass    

        # Not sure what it does, seems like the center of the object decides the direction
        if self.type == "bounceDirection":
            self.bounceDirection()
            pass    

        # Sprite tries to move in the opposite direction of partner
        if self.type == "bounceForward":
            self.bounceForward()
            pass    

        # Change resource (sprite) in the object (partner) to a given
        if self.type == "changeResource":
            self.changeResource()
            pass

        # Creates a copy
        if self.type == "cloneSprite":
            self.cloneSprite()
            pass

        # Increment resource (sprite) in the object (partner)
        if self.type == "collectResource":
            self.collectResource()
            pass    

        # [GVGAI] Decrease speed of all objects of the type of the sprite
        if self.type == "decreaseSpeedToAll":
            self.decreaseSpeedToAll()
            pass    

        # Changes to a random orientation
        if self.type == "flipDirection":
            self.flipDirection()
            pass

        # [GVGAI] Increase speed of all objects of the sprite type
        if self.type == "increaseSpeedToAll":
            self.increaseSpeedToAll()
            pass    

        # [GVGAI] Kill all sprite of the same type
        if self.type == "killAll":
            self.killAll()
            pass        

        # Sprite and partner dies
        if self.type == "killBoth":
            self.killBoth()
            pass

        # Kill sprite if partner is not destroyed by the collision
        if self.type == "killIfAlive":
            self.killIfAlive()
            pass    

        # Kill sprite if partner is above him
        if self.type == "killIfFromAbove":
            self.killIfFromAbove()
            pass        

        # If sprite has more resource than parameter (limit), kill it
        if self.type == "killIfHasMore":
            self.killIfHasMore()
            pass    

        # Not found in the GVGAI files
        # If sprite has less resource than parameter (limit), kill it
        # if self.type == "killIfHasLess":
            # pass    

        # Kill sprite if speed is higher than the given
        if self.type == "killIfFast":
            self.killIfFast()
            pass    

        # If partner has less resource than parameter (limit), kill sprite
        if self.type == "killIfOtherHasLess":
            self.killIfOtherHasLess()
            pass

        # If partner has more resource than parameter (limit), kill sprite
        if self.type == "killIfOtherHasMore":
            self.killIfOtherHasMore()
            pass

        # Kill sprite if speed is lower than the given
        if self.type == "killIfSlow":
            self.killIfSlow()
            pass    

        # Sprite dies
        if self.type == "killSprite":
            self.killSprite()
            pass

        # Movement of partner is added to sprite (same quantity and direction)
        if self.type == "pullWithIt":
            self.pullWithIt()
            pass

        # [GVGAI] Changes score of the avatar
        if self.type == "removeScore":
            self.removeScore()
            pass    

        # Changes orientation 180º
        if self.type == "reverseDirection":
            self.reverseDirection()
            pass

        # [GVGAI] Asigns a specific speed to the sprite
        if self.type == "setSpeedToAll":
            self.setSpeedToAll()
            pass    

        # Creates sprite behind partner
        if self.type == "spawnBehind":
            self.spawnBehind()
            pass    

        # If sprite has less resource than parameter (limit), create new sprite
        if self.type == "spawnIfHasLess":
            self.spawnIfHasLess()
            pass

        # If sprite has more resource than parameter (limit), create new sprite
        if self.type == "spawnIfHasMore":
            self.spawnIfHasMore()
            pass

        # Undo last movement
        if self.type == "stepBack":
            self.stepBack()
            pass

        # [GVGAI] Decrease a certain quantity of health points
        if self.type == "substractHealthPoints":
            self.subsctractHealthPoints()
            pass    

        # Move sprite to partner position (must be a Portal, if not, destroy sprite)
        if self.type == "teleportToExit":
            self.teleportToExit()
            pass    

        # [GVGAI] Changes sprite to stype if there are a certain quantity (stypeCount)
        if self.type == "transformIfCount":
            self.transformIfCounts()
            pass

        # Seems like it creates a new copy of sprite
        if self.type == "transformTo":
            self.transformTo()
            pass

        # [GVGAI] Transform sprite to one of his childs
        if self.type == "transformToRandomChild":
            self.transformToRandomChild()
            pass

        # [GVGAI] Transform all sprites of stype to stype_other in the same position
        if self.type == "transformToSingleton":
            self.transformToSingleton()
            pass

        # Not sure what it does, in VGDL seems to call reverseDirection
        if self.type == "turnAround":
            self.turnAround()
            pass

        # Undo movement of every object in the game
        if self.type == "undoAll":
            self.undoAll()
            pass

        # [GVGAI] Changes the "spawn type" to SpawnPoint
        if self.type == "updateSpawnType":
            self.updateSpawnType()
            pass    

        # Bounce in a perpendicular direction from the wall
        if self.type == "wallBounce":
            self.wallBounce()
            pass        

        # Stops sprite in front of wall
        if self.type == "wallStop":
            self.wallStop()
            pass

        # Move sprite at the end of the screen in the orientation of sprite
        if self.type == "wrapAround":
            self.wrapAround()
            pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    # UNFINISHED
    def addHealthPoints(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_addhealthpoints"
        # preconditions = [["(evaluate-interaction " + self.sprite_name + " - " +
        #                     self.sprite_type + " " + self.partner_name + " - " +
        #                     self.partner_type + ")"],
        preconditions = [["(evaluate-interation ?x - " + self.sprite_type + 
                            " " + "?y " + self.partner_type + ")"],
                         ["(not (= (coordinate_x ?x) -1))"],
                         ["(not (= (coordinate_x ?y) -1))"]]
        tasks         = [["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_ADDHEALTHPOINTS ?x ?y)"],
                        ["(:inline () (not (evaluate-interation ?x - " + self.sprite_type + 
                            " " + "?y " + self.partner_type + ")))"],
                        ["(:inline () (regenerate-interation ?x - " + self.sprite_type + 
                            " " + "?y " + self.partner_type + "))"],
                        ["(check-interactions)"]]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def addHealthPointsToMax(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_addhealthpointstomax"  
        preconditions = [["(evaluate-interation ?x - " + self.sprite_type + 
                            " " + "?y " + self.partner_type + ")"],
                         ["(not (= (coordinate_x ?x) -1))"],
                         ["(not (= (coordinate_x ?y) -1))"]]
        tasks         = [["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_ADDHEALTHPOINTSTOMAX ?x ?y)"],
                        ["(:inline () (not (evaluate-interation ?x - " + self.sprite_type + 
                            " " + "?y " + self.partner_type + ")))"],
                        ["(:inline () (regenerate-interation ?x - " + self.sprite_type + 
                            " " + "?y " + self.partner_type + "))"],
                        ["(check-interactions)"]]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def align(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_align"  
        preconditions = [["(evaluate-interation ?x - " + self.sprite_type + 
                            " " + "?y " + self.partner_type + ")"],
                         ["(not (= (coordinate_x ?x) -1))"],
                         ["(not (= (coordinate_x ?y) -1))"]]
        tasks         = [["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_ALIGN ?x ?y)"],
                        ["(:inline () (not (evaluate-interation ?x - " + self.sprite_type + 
                            " " + "?y " + self.partner_type + ")))"],
                        ["(:inline () (regenerate-interation ?x - " + self.sprite_type + 
                            " " + "?y " + self.partner_type + "))"],
                        ["(check-interactions)"]]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def attractGaze(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_ATTRACTGAZE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def bounceDirection(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_BOUNCEDIRECTION"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def bounceForward(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_BOUNCEFORWARD"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def changeResource(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_CHANGERESOURCE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def cloneSprite(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_CLONESPRITE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def collectResource(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_COLLECTRESOURCE"
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

    # UNFINISHED
    def decreaseSpeedToAll(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_INCREASESPEEDTOALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def flipDirection(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_FLIPDIRECTION"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def increaseSpeedToAll(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_INCREASESPEEDTOALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killAll(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killBoth(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLBOTH"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfAlive(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFALIVE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfFromAbove(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFFROMABOVE"
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

    # UNFINISHED
    def killIfHasMore(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFHASMORE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfFast(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFFAST"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfOtherHasLess(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFOTHERHASLESS"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfOtherHasMore(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFOTHERHASMORE"
        # + self.third_sprite_type.upper() FIND TYPE IN PARAMETERS OF ACTION
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfSlow(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFSLOW"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killSprite(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLSPRITE"        
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

    # UNFINISHED
    def pullWithIt(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_PULLWITHIT"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def removeScore(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_REMOVESCORE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def reverseDirection(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_REVERSEDIRECTION"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def setSpeedToAll(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_SETSPEEDTOALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def spawnBehind(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_SPAWNBEHING"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def spawnIfHasLess(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_SPAWNIFHASLESS"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def spawnIfHasMore(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_SPAWNIFHASMORE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def stepBack(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_STEPBACK"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [["(assign (coordinate_y ?x) (last_coordinate_x ?x))"],
					["(assign (coordinate_y ?x) (last_coordinate_y ?x))"]]

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def subsctractHealthPoints(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_SUBSCTRACTHEALTHPOINTS"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def teleportToExit(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TELEPORTTOEXIT"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def transformIfCount(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TRANSFORMIFCOUNT"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def transformTo(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TRANSFORMTO"
                # + self.third_sprite_type.upper() FIND TYPE IN PARAMETERS OF ACTION
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def transformToRandomChild(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TRANSFORMTORANDOMCHILD"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def transformToSingleton(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TRANSFORMTOSINGLETON"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def turnAround(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TURNAROUND"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def undoAll(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_UNDOALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def updateSpawnType(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_UPDATESPAWNTYPE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def wallBounce(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_WALLBOUNCE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def wallStop(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_WALLSTOP"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def wrapAround(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_WRAPAROUND"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class InteractionActions:
    """ Returns an action for each interaction """
    def __init__(self, interaction_type,
                       sprite_name, sprite_stype, 
                       partner_name, partner_stype,
                       parameters):

        self.sprite_name  = sprite_name
        self.sprite_type  = sprite_stype
        self.partner_name = partner_name
        self.partner_type = partner_stype    
        self.type         = interaction_type
        self.parameters   = parameters

    def get_actions(self):
        """ Return a list of actions depending of the interaction """
        actions = []

        # [GVGAI] Adds a certain quantity of health points
        if self.type == "addHealthPoints":
            self.addHealthPoints()
            pass    

        # [GVGAI] Puts health points to max
        if self.type == "addHealthPointsToMax":
            self.addHealthPointsToMax()
            pass    

        # [GVGAI] Changes position and orientation of sprite to partner
        if self.type == "align":
            self.align()
            pass    

        # Randomly changesdirection of partner
        if self.type == "attractGaze":
            self.attractGaze()
            pass    

        # Not sure what it does, seems like the center of the object decides the direction
        if self.type == "bounceDirection":
            self.bounceDirection()
            pass    

        # Sprite tries to move in the opposite direction of partner
        if self.type == "bounceForward":
            self.bounceForward()
            pass    

        # Change resource (sprite) in the object (partner) to a given
        if self.type == "changeResource":
            self.changeResource()
            pass

        # Creates a copy
        if self.type == "cloneSprite":
            self.cloneSprite()
            pass

        # Increment resource (sprite) in the object (partner)
        if self.type == "collectResource":
            self.collectResource()
            pass    

        # [GVGAI] Decrease speed of all objects of the type of the sprite
        if self.type == "decreaseSpeedToAll":
            self.decreaseSpeedToAll()
            pass    

        # Changes to a random orientation
        if self.type == "flipDirection":
            self.flipDirection()
            pass

        # [GVGAI] Increase speed of all objects of the sprite type
        if self.type == "increaseSpeedToAll":
            self.increaseSpeedToAll()
            pass    

        # [GVGAI] Kill all sprite of the same type
        if self.type == "killAll":
            self.killAll()
            pass        

        # Sprite and partner dies
        if self.type == "killBoth":
            self.killBoth()
            pass

        # Kill sprite if partner is not destroyed by the collision
        if self.type == "killIfAlive":
            self.killIfAlive()
            pass    

        # Kill sprite if partner is above him
        if self.type == "killIfFromAbove":
            self.killIfFromAbove()
            pass        

        # If sprite has more resource than parameter (limit), kill it
        if self.type == "killIfHasMore":
            self.killIfHasMore()
            pass    

        # Not found in the GVGAI files
        # If sprite has less resource than parameter (limit), kill it
        # if self.type == "killIfHasLess":
            # pass    

        # Kill sprite if speed is higher than the given
        if self.type == "killIfFast":
            self.killIfFast()
            pass    

        # If partner has less resource than parameter (limit), kill sprite
        if self.type == "killIfOtherHasLess":
            self.killIfOtherHasLess()
            pass

        # If partner has more resource than parameter (limit), kill sprite
        if self.type == "killIfOtherHasMore":
            self.killIfOtherHasMore()
            pass

        # Kill sprite if speed is lower than the given
        if self.type == "killIfSlow":
            self.killIfSlow()
            pass    

        # Sprite dies
        if self.type == "killSprite":
            self.killSprite()
            pass

        # Movement of partner is added to sprite (same quantity and direction)
        if self.type == "pullWithIt":
            self.pullWithIt()
            pass

        # [GVGAI] Changes score of the avatar
        if self.type == "removeScore":
            self.removeScore()
            pass    

        # Changes orientation 180º
        if self.type == "reverseDirection":
            self.reverseDirection()
            pass

        # [GVGAI] Asigns a specific speed to the sprite
        if self.type == "setSpeedToAll":
            self.setSpeedToAll()
            pass    

        # Creates sprite behind partner
        if self.type == "spawnBehind":
            self.spawnBehind()
            pass    

        # If sprite has less resource than parameter (limit), create new sprite
        if self.type == "spawnIfHasLess":
            self.spawnIfHasLess()
            pass

        # If sprite has more resource than parameter (limit), create new sprite
        if self.type == "spawnIfHasMore":
            self.spawnIfHasMore()
            pass

        # Undo last movement
        if self.type == "stepBack":
            self.stepBack()
            pass

        # [GVGAI] Decrease a certain quantity of health points
        if self.type == "substractHealthPoints":
            self.subsctractHealthPoints()
            pass    

        # Move sprite to partner position (must be a Portal, if not, destroy sprite)
        if self.type == "teleportToExit":
            self.teleportToExit()
            pass    

        # [GVGAI] Changes sprite to stype if there are a certain quantity (stypeCount)
        if self.type == "transformIfCount":
            self.transformIfCounts()
            pass

        # Seems like it creates a new copy of sprite
        if self.type == "transformTo":
            self.transformTo()
            pass

        # [GVGAI] Transform sprite to one of his childs
        if self.type == "transformToRandomChild":
            self.transformToRandomChild()
            pass

        # [GVGAI] Transform all sprites of stype to stype_other in the same position
        if self.type == "transformToSingleton":
            self.transformToSingleton()
            pass

        # Not sure what it does, in VGDL seems to call reverseDirection
        if self.type == "turnAround":
            self.turnAround()
            pass

        # Undo movement of every object in the game
        if self.type == "undoAll":
            self.undoAll()
            pass

        # [GVGAI] Changes the "spawn type" to SpawnPoint
        if self.type == "updateSpawnType":
            self.updateSpawnType()
            pass    

        # Bounce in a perpendicular direction from the wall
        if self.type == "wallBounce":
            self.wallBounce()
            pass        

        # Stops sprite in front of wall
        if self.type == "wallStop":
            self.wallStop()
            pass

        # Move sprite at the end of the screen in the orientation of sprite
        if self.type == "wrapAround":
            self.wrapAround()
            pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def addHealthPoints(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_ADDHEALTHPOINTS"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def addHealthPointsToMax(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_ADDHEALTHPOINTSTOMAX"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def align(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_ALIGN"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def attractGaze(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_ATTRACTGAZE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def bounceDirection(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_BOUNCEDIRECTION"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def bounceForward(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_BOUNCEFORWARD"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def changeResource(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_CHANGERESOURCE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def cloneSprite(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_CLONESPRITE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def collectResource(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_COLLECTRESOURCE"
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
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_INCREASESPEEDTOALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def flipDirection(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_FLIPDIRECTION"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def increaseSpeedToAll(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_INCREASESPEEDTOALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killAll(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killBoth(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLBOTH"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfAlive(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFALIVE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfFromAbove(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFFROMABOVE"
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
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFHASMORE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfFast(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFFAST"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfOtherHasLess(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFOTHERHASLESS"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfOtherHasMore(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFOTHERHASMORE"
        # + self.third_sprite_type.upper() FIND TYPE IN PARAMETERS OF ACTION
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfSlow(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFSLOW"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killSprite(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLSPRITE"        
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
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_PULLWITHIT"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def removeScore(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_REMOVESCORE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def reverseDirection(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_REVERSEDIRECTION"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def setSpeedToAll(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_SETSPEEDTOALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def spawnBehind(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_SPAWNBEHING"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def spawnIfHasLess(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_SPAWNIFHASLESS"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def spawnIfHasMore(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_SPAWNIFHASMORE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def stepBack(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_STEPBACK"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [["(assign (coordinate_y ?x) (last_coordinate_x ?x))"],
					["(assign (coordinate_y ?x) (last_coordinate_y ?x))"]]

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def subsctractHealthPoints(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_SUBSCTRACTHEALTHPOINTS"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def teleportToExit(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TELEPORTTOEXIT"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def transformIfCount(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TRANSFORMIFCOUNT"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def transformTo(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TRANSFORMTO"
                # + self.third_sprite_type.upper() FIND TYPE IN PARAMETERS OF ACTION
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def transformToRandomChild(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TRANSFORMTORANDOMCHILD"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def transformToSingleton(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TRANSFORMTOSINGLETON"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def turnAround(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TURNAROUND"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def undoAll(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_UNDOALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def updateSpawnType(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_UPDATESPAWNTYPE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def wallBounce(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_WALLBOUNCE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def wallStop(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_WALLSTOP"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def wrapAround(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_WRAPAROUND"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = [["(= (coordinate_x ?x) (coordinate_x ?y))"],
                      ["(= (coordinate_y ?x) (coordinate_y ?y))"]]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        