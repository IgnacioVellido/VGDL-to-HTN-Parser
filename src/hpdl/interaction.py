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
        # Generic task, not needed
        # self.task     = InteractionTasks(methods).get_tasks()
        # self.predicates =

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

# class InteractionTasks:
#     """ Creates the tasks for checking interactions """
#     def __init__(self, actions):
#         self.actions = actions

#     def get_tasks(self):
#         pass
 
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
        """ Return a method depending of the interaction """

        # [GVGAI] Adds a certain quantity of health points
        if self.type == "addHealthPoints":
            return self.addHealthPoints() 

        # [GVGAI] Puts health points to max
        if self.type == "addHealthPointsToMax":
            return self.addHealthPointsToMax()

        # [GVGAI] Changes position and orientation of sprite to partner
        if self.type == "align":
            return self.align() 

        # Randomly changesdirection of partner
        if self.type == "attractGaze":
            return self.attractGaze() 

        # Not sure what it does, seems like the center of the object decides the direction
        if self.type == "bounceDirection":
            return self.bounceDirection() 

        # Sprite tries to move in the opposite direction of partner
        if self.type == "bounceForward":
            return self.bounceForward() 

        # Change resource (sprite) in the object (partner) to a given
        if self.type == "changeResource":
            return self.changeResource()

        # Creates a copy
        if self.type == "cloneSprite":
            return self.cloneSprite()

        # Increment resource (sprite) in the object (partner)
        if self.type == "collectResource":
            return self.collectResource() 

        # [GVGAI] Decrease speed of all objects of the type of the sprite
        if self.type == "decreaseSpeedToAll":
            return self.decreaseSpeedToAll()

        # Changes to a random orientation
        if self.type == "flipDirection":
            return self.flipDirection()

        # [GVGAI] Increase speed of all objects of the sprite type
        if self.type == "increaseSpeedToAll":
            return self.increaseSpeedToAll()

        # [GVGAI] Kill all sprite of the same type
        if self.type == "killAll":
            return self.killAll()

        # Sprite and partner dies
        if self.type == "killBoth":
            return self.killBoth()

        # Kill sprite if partner is not destroyed by the collision
        if self.type == "killIfAlive":
            return self.killIfAlive() 

        # Kill sprite if partner is above him
        if self.type == "killIfFromAbove":
            return self.killIfFromAbove()

        # If sprite has more resource than parameter (limit), kill it
        if self.type == "killIfHasMore":
            return self.killIfHasMore() 

        # Not found in the GVGAI files
        # If sprite has less resource than parameter (limit), kill it
        # if self.type == "killIfHasLess":
            # pass    

        # Kill sprite if speed is higher than the given
        if self.type == "killIfFast":
            return self.killIfFast() 

        # If partner has less resource than parameter (limit), kill sprite
        if self.type == "killIfOtherHasLess":
            return self.killIfOtherHasLess()

        # If partner has more resource than parameter (limit), kill sprite
        if self.type == "killIfOtherHasMore":
            return self.killIfOtherHasMore()

        # Kill sprite if speed is lower than the given
        if self.type == "killIfSlow":
            return self.killIfSlow() 

        # Sprite dies
        if self.type == "killSprite":
            return self.killSprite()

        # Movement of partner is added to sprite (same quantity and direction)
        if self.type == "pullWithIt":
            return self.pullWithIt()

        # [GVGAI] Changes score of the avatar
        if self.type == "removeScore":
            return self.removeScore() 

        # Changes orientation 180º
        if self.type == "reverseDirection":
            return self.reverseDirection()

        # [GVGAI] Asigns a specific speed to the sprite
        if self.type == "setSpeedToAll":
            return self.setSpeedToAll()

        # Creates sprite behind partner
        if self.type == "spawnBehind":
            return self.spawnBehind() 

        # If sprite has less resource than parameter (limit), create new sprite
        if self.type == "spawnIfHasLess":
            return self.spawnIfHasLess()

        # If sprite has more resource than parameter (limit), create new sprite
        if self.type == "spawnIfHasMore":
            return self.spawnIfHasMore()

        # Undo last movement
        if self.type == "stepBack":
            return self.stepBack()

        # [GVGAI] Decrease a certain quantity of health points
        if self.type == "substractHealthPoints":
            return self.subsctractHealthPoints() 

        # Move sprite to partner position (must be a Portal, if not, destroy sprite)
        if self.type == "teleportToExit":
            return self.teleportToExit() 

        # [GVGAI] Changes sprite to stype if there are a certain quantity (stypeCount)
        if self.type == "transformIfCount":
            return self.transformIfCounts()

        # Seems like it creates a new copy of sprite
        if self.type == "transformTo":
            return self.transformTo()

        # [GVGAI] Transform sprite to one of his childs
        if self.type == "transformToRandomChild":
            return self.transformToRandomChild()

        # [GVGAI] Transform all sprites of stype to stype_other in the same position
        if self.type == "transformToSingleton":
            return self.transformToSingleton()

        # Not sure what it does, in VGDL seems to call reverseDirection
        if self.type == "turnAround":
            return self.turnAround()

        # Undo movement of every object in the game
        if self.type == "undoAll":
            return self.undoAll()

        # [GVGAI] Changes the "spawn type" to SpawnPoint
        if self.type == "updateSpawnType":
            return self.updateSpawnType() 

        # Bounce in a perpendicular direction from the wall
        if self.type == "wallBounce":
            return self.wallBounce()     

        # Stops sprite in front of wall
        if self.type == "wallStop":
            return self.wallStop()

        # Move sprite at the end of the screen in the orientation of sprite
        if self.type == "wrapAround":
            return self.wrapAround()

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    # UNFINISHED
    def addHealthPoints(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_addhealthpoints"
        # preconditions = ["(evaluate-interaction " + self.sprite_name + " - " +
        #                     self.sprite_type + " " + self.partner_name + " - " +
        #                     self.partner_type + ")"],
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_ADDHEALTHPOINTS ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def addHealthPointsToMax(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_addhealthpointstomax"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_ADDHEALTHPOINTSTOMAX ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def align(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_align"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_ALIGN ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def attractGaze(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_attractgaze"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_ATTRACTGAZE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)       

    # -------------------------------------------------------------------------

    # UNFINISHED
    def bounceDirection(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_bouncedirection"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_BOUNCEDIRECTION ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def bounceForward(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_bounceforward"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_BOUNCEFORWARD ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def changeResource(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_changeresource"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_CHANGERESOURCE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def cloneSprite(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_clonesprite"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_CLONESPRITE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def collectResource(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_collectresource"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_COLLECTRESOURCE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def decreaseSpeedToAll(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_decreasespeedtoall"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_DECREASESPEEDTOALL ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def flipDirection(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_flipdirection"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_FLIPDIRECTION ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)  

    # -------------------------------------------------------------------------

    # UNFINISHED
    def increaseSpeedToAll(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_increasespeedtoall"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_INCREASESPEEDTOALL ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killAll(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_killall"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_KILLALL ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killBoth(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_killboth"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_KILLBOTH ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfAlive(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_killifalive"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_KILLIFALIVE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfFromAbove(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_killiffromabove"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_KILLIFFROMABOVE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfHasMore(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_killifhasmore"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_KILLIFHASMORE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfFast(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_killiffast"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_KILLIFFAST ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfOtherHasLess(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_killifotherhasless"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_KILLIFOTHERHASLESS ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    # NEEDED REST OF THE NAME
    def killIfOtherHasMore(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_killifotherhasmore"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_KILLIFOTHERHASMORE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfSlow(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_killifslow"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_KILLIFSLOW ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killSprite(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_killsprite"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_KILLSPRITE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def pullWithIt(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_pullwithit"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_PULLWITHIT ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def removeScore(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_removescore"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_REMOVESCORE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def reverseDirection(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_reversedirection"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_REVERSEDIRECTION ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def setSpeedToAll(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_setspeedtoall"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_SETSPEEDTOALL ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def spawnBehind(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_spawnbehind"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_SPAWNBEHIND ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def spawnIfHasLess(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_spawnifhasless"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_SPAWNIFHASLESS ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def spawnIfHasMore(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_spawnifhasmore"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_SPAWNIFHASMORE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def stepBack(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_stepback"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_STEPBACK ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def subsctractHealthPoints(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_substracthealthpoints"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_SUBSTRACTHEALTHPOINTS ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def teleportToExit(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_teleporttoexit"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_TELEPORTTOEXIT ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def transformIfCount(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_transformifcount"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_TRANSFORMIFCOUNT ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    # NEEDED REST OF THE NAME
    def transformTo(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_transformto"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_TRANSFORMTO ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def transformToRandomChild(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_transformtorandomchild"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_TRANSFORMTORANDOMCHILD ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def transformToSingleton(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_transformtosingleton"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_TRANSFORMTOSINGLETON ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def turnAround(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_turnaround"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_TURNAROUND ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def undoAll(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_undoall"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_UNDOALL ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def updateSpawnType(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_updatespawntype"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_UPDATESPAWNTYPE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def wallBounce(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_wallbounce"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_WALLBOUNCE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def wallStop(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_WALLSTOP"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_WALLSTOP ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def wrapAround(self):
        name = self.sprite_name.lower() + "_" + self.partner_name.lower() + "_wraparound"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite_name.upper() + "_" 
                            + self.partner_name.upper() 
                            + "_WRAPAROUND ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite_type + 
                            " " + "?y - " + self.partner_type + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class InteractionActions:
    """ Returns an action for each interaction """
    def __init__(self, sprite_name, sprite_stype, 
                       partner_name, partner_stype,
                       interaction, parameters,
                       hierarchy):

        self.sprite_name  = sprite_name
        self.sprite_type  = sprite_stype
        self.partner_name = partner_name
        self.partner_type = partner_stype    
        self.type         = interaction
        self.parameters   = parameters
        self.hierarchy    = hierarchy

    def get_actions(self):
        """ Return an action depending of the interaction """
        # [GVGAI] Adds a certain quantity of health points
        if self.type == "addHealthPoints":
            return self.addHealthPoints() 

        # [GVGAI] Puts health points to max
        if self.type == "addHealthPointsToMax":
            return self.addHealthPointsToMax() 

        # [GVGAI] Changes position and orientation of sprite to partner
        if self.type == "align":
            return self.align() 

        # Randomly changesdirection of partner
        if self.type == "attractGaze":
            return self.attractGaze()

        # Not sure what it does, seems like the center of the object decides the direction
        if self.type == "bounceDirection":
            return self.bounceDirection() 

        # Sprite tries to move in the opposite direction of partner
        if self.type == "bounceForward":
            return self.bounceForward() 

        # Change resource (sprite) in the object (partner) to a given
        if self.type == "changeResource":
            return self.changeResource()

        # Creates a copy
        if self.type == "cloneSprite":
            return self.cloneSprite()

        # Increment resource (sprite) in the object (partner)
        if self.type == "collectResource":
            return self.collectResource() 

        # [GVGAI] Decrease speed of all objects of the type of the sprite
        if self.type == "decreaseSpeedToAll":
            return self.decreaseSpeedToAll() 

        # Changes to a random orientation
        if self.type == "flipDirection":
            return self.flipDirection()

        # [GVGAI] Increase speed of all objects of the sprite type
        if self.type == "increaseSpeedToAll":
            return self.increaseSpeedToAll() 

        # [GVGAI] Kill all sprite of the same type
        if self.type == "killAll":
            return self.killAll()     

        # Sprite and partner dies
        if self.type == "killBoth":
            return self.killBoth()

        # Kill sprite if partner is not destroyed by the collision
        if self.type == "killIfAlive":
            return self.killIfAlive() 

        # Kill sprite if partner is above him
        if self.type == "killIfFromAbove":
            return self.killIfFromAbove()

        # If sprite has more resource than parameter (limit), kill it
        if self.type == "killIfHasMore":
            return self.killIfHasMore() 

        # Not found in the GVGAI files
        # If sprite has less resource than parameter (limit), kill it
        # if self.type == "killIfHasLess":
            # pass    

        # Kill sprite if speed is higher than the given
        if self.type == "killIfFast":
            return self.killIfFast() 

        # If partner has less resource than parameter (limit), kill sprite
        if self.type == "killIfOtherHasLess":
            return self.killIfOtherHasLess()

        # If partner has more resource than parameter (limit), kill sprite
        if self.type == "killIfOtherHasMore":
            return self.killIfOtherHasMore()

        # Kill sprite if speed is lower than the given
        if self.type == "killIfSlow":
            return self.killIfSlow() 

        # Sprite dies
        if self.type == "killSprite":
            return self.killSprite()

        # Movement of partner is added to sprite (same quantity and direction)
        if self.type == "pullWithIt":
            return self.pullWithIt()

        # [GVGAI] Changes score of the avatar
        if self.type == "removeScore":
            return self.removeScore() 

        # Changes orientation 180º
        if self.type == "reverseDirection":
            return self.reverseDirection()

        # [GVGAI] Asigns a specific speed to the sprite
        if self.type == "setSpeedToAll":
            return self.setSpeedToAll() 

        # Creates sprite behind partner
        if self.type == "spawnBehind":
            return self.spawnBehind() 

        # If sprite has less resource than parameter (limit), create new sprite
        if self.type == "spawnIfHasLess":
            return self.spawnIfHasLess()

        # If sprite has more resource than parameter (limit), create new sprite
        if self.type == "spawnIfHasMore":
            return self.spawnIfHasMore()

        # Undo last movement
        if self.type == "stepBack":
            return self.stepBack()

        # [GVGAI] Decrease a certain quantity of health points
        if self.type == "substractHealthPoints":
            return self.subsctractHealthPoints() 

        # Move sprite to partner position (must be a Portal, if not, destroy sprite)
        if self.type == "teleportToExit":
            return self.teleportToExit() 

        # [GVGAI] Changes sprite to stype if there are a certain quantity (stypeCount)
        if self.type == "transformIfCount":
            return self.transformIfCounts()

        # Seems like it creates a new copy of sprite
        if self.type == "transformTo":
            return self.transformTo()

        # [GVGAI] Transform sprite to one of his childs
        if self.type == "transformToRandomChild":
            return self.transformToRandomChild()

        # [GVGAI] Transform all sprites of stype to stype_other in the same position
        if self.type == "transformToSingleton":
            return self.transformToSingleton()

        # Not sure what it does, in VGDL seems to call reverseDirection
        if self.type == "turnAround":
            return self.turnAround()

        # Undo movement of every object in the game
        if self.type == "undoAll":
            return self.undoAll()

        # [GVGAI] Changes the "spawn type" to SpawnPoint
        if self.type == "updateSpawnType":
            return self.updateSpawnType() 

        # Bounce in a perpendicular direction from the wall
        if self.type == "wallBounce":
            return self.wallBounce()     

        # Stops sprite in front of wall
        if self.type == "wallStop":
            return self.wallStop()

        # Move sprite at the end of the screen in the orientation of sprite
        if self.type == "wrapAround":
            return self.wrapAround()

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def addHealthPoints(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_ADDHEALTHPOINTS"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def addHealthPointsToMax(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_ADDHEALTHPOINTSTOMAX"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def align(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_ALIGN"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def attractGaze(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_ATTRACTGAZE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def bounceDirection(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_BOUNCEDIRECTION"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def bounceForward(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_BOUNCEFORWARD"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def changeResource(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_CHANGERESOURCE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def cloneSprite(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_CLONESPRITE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def collectResource(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_COLLECTRESOURCE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = ["(assign (last_coordinate_y ?x) (coordinate_x ?x))",
					"(assign (last_coordinate_y ?x) (coordinate_y ?x))",
					"(assign (coordinate_x ?x) -1)",
					"(assign (coordinate_y ?x) -1)",
					"(decrease (counter_" + self.sprite_type + ") 1)",
					"(decrease (counter_Resource) 1)",
					"(decrease (counter_Object) 1)",

					"(increase (resource_" + self.sprite_name + " ?a) 1)"]

        for parent in self.hierarchy[self.sprite_type]:
            effects.append("(decrease (counter_" + parent + ") 1)")

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def decreaseSpeedToAll(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_INCREASESPEEDTOALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def flipDirection(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_FLIPDIRECTION"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def increaseSpeedToAll(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_INCREASESPEEDTOALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killAll(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killBoth(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLBOTH"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = ["(assign (last_coordinate_x ?x) (coordinate_x ?x))",
                   "(assign (last_coordinate_y ?x) (coordinate_y ?x))",
                   "(assign (last_coordinate_x ?y) (coordinate_x ?y))",
                   "(assign (coordinate_x ?x) -1)",
                   "(assign (coordinate_y ?x) -1)",
                   "(assign (coordinate_x ?y) -1)",
                   "(assign (coordinate_y ?y) -1)",
                   "(decrease (counter_" + self.sprite_type + ") 1)",                       
                   "(decrease (counter_" + self.partner_type + ") 1)",
                   ]

        for parent in self.hierarchy[self.sprite_type]:
            effects.append("(decrease (counter_" + parent + ") 1)")

        for parent in self.hierarchy[self.partner_type]:
            effects.append("(decrease (counter_" + parent + ") 1)")

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfAlive(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFALIVE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------
    
    def killIfFromAbove(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFFROMABOVE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))",
                      "(= (last_coordinate_y ?y) (- (coordinate_y ?y) 1))"]
        effects = ["(assign (last_coordinate_y ?a) (coordinate_x ?a))",
					"(assign (last_coordinate_y ?a) (coordinate_y ?a))",
					"(assign (coordinate_x ?a) -1)",
					"(assign (coordinate_y ?a) -1)",
					"(decrease (counter_" + self.sprite_type + ") 1)",
					"(decrease (counter_Object) 1)"]

        for parent in self.hierarchy[self.sprite_type]:
            effects.append("(decrease (counter_" + parent + ") 1)")

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfHasMore(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFHASMORE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfFast(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFFAST"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfOtherHasLess(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFOTHERHASLESS"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfOtherHasMore(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFOTHERHASMORE"
        # + self.third_sprite_type.upper() FIND TYPE IN PARAMETERS OF ACTION
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfSlow(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLIFSLOW"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killSprite(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_KILLSPRITE"        
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [ "(assign (last_coordinate_y ?x) (coordinate_x ?x))",
					"(assign (last_coordinate_y ?x) (coordinate_y ?x))",
					"(assign (coordinate_x ?x) -1)",
					"(assign (coordinate_y ?x) -1)",

					"(decrease (counter_" + self.sprite_type + ") 1)",					
					"(decrease (counter_Object) 1)"]

        for parent in self.hierarchy[self.sprite_type]:
            effects.append("(decrease (counter_" + parent + ") 1)")

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def pullWithIt(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_PULLWITHIT"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def removeScore(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_REMOVESCORE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def reverseDirection(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_REVERSEDIRECTION"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def setSpeedToAll(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_SETSPEEDTOALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def spawnBehind(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_SPAWNBEHING"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def spawnIfHasLess(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_SPAWNIFHASLESS"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def spawnIfHasMore(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_SPAWNIFHASMORE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # Finished
    def stepBack(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_STEPBACK"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = ["(assign (coordinate_y ?x) (last_coordinate_x ?x))",
					"(assign (coordinate_y ?x) (last_coordinate_y ?x))"]

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def subsctractHealthPoints(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_SUBSCTRACTHEALTHPOINTS"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def teleportToExit(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TELEPORTTOEXIT"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def transformIfCount(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TRANSFORMIFCOUNT"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def transformTo(self):
        # Find object to tranform
        # third_sprite = 

        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TRANSFORMTO"
                # + self.third_sprite_type.upper() FIND TYPE IN PARAMETERS OF ACTION
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]#, ["z", third_sprite_type]]
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        
        effects = ["(assign (last_coordinate_x ?x) (coordinate_x ?x))",
                   "(assign (last_coordinate_y ?x) (coordinate_y ?x))",
                   "(assign (last_coordinate_x ?y) (coordinate_x ?y))",
                   "(assign (coordinate_x ?x) -1)",
                   "(assign (coordinate_y ?x) -1)",
                   "(assign (coordinate_x ?y) -1)",
                   "(assign (coordinate_y ?y) -1)",
                   "(decrease (counter_" + self.sprite_type + ") 1)",                       
                   "(decrease (counter_" + self.partner_type + ") 1)",

                    # Last coordinate is -1, no need to assign (is non-existen object)
                   "(assign (coordinate_x ?z) (last_coordinate_x ?x))",
                   "(assign (coordinate_y ?z) (last_coordinate_y ?x))"
                #    "(increase (counter_" + third_sprite_type + ") 1)"
                   ]

        for parent in self.hierarchy[self.sprite_type]:
            effects.append("(decrease (counter_" + parent + ") 1)")

        for parent in self.hierarchy[self.partner_type]:
            effects.append("(decrease (counter_" + parent + ") 1)")

        # for parent in self.hierarchy[self.third_sprite_type]:
        #     effects.append("(increase (counter_" + parent + ") 1)")

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def transformToRandomChild(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TRANSFORMTORANDOMCHILD"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def transformToSingleton(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TRANSFORMTOSINGLETON"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def turnAround(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_TURNAROUND"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def undoAll(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_UNDOALL"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def updateSpawnType(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_UPDATESPAWNTYPE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def wallBounce(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_WALLBOUNCE"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def wallStop(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_WALLSTOP"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def wrapAround(self):
        name = self.sprite_name.upper() + "_" + self.partner_name.upper() + "_WRAPAROUND"
        parameters = [["x", self.sprite_name], ["y", self.partner_type]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)