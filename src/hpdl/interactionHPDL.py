###############################################################################
# interaction.py
# Ignacio Vellido Expósito
# 09/09/2019
# 
# Multiple classes defining parts of a HPDL domain for interactions
###############################################################################

from hpdl.typesHPDL import *

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class InteractionHPDL:
    """ Class that encapsulate the generation of HPDL domain structures 
    for interactions 
    
    Atributes:
        interaction - InteractioVGDL
        sprite - SpriteVGDL

    """
    # def __init__(self, interaction_type, 
    #              sprite_name, sprite_stype, 
    #              partner_name, partner_stype,
    #              parameters):
    def __init__(self, interaction, sprite, partner, hierarchy):
        self.interaction = interaction
        self.sprite      = sprite
        self.partner     = partner
        self.hierarchy   = hierarchy

        self.tasks              = []        
        self.methods            = []
        self.actions            = []
        self.predicates         = []
        self.level_predicates   = []

        self.get_actions()
        self.get_methods()
        self.get_tasks()
        self.get_predicates()
        self.get_level_predicates()

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def get_actions(self):
        self.actions = InteractionMethods(self.interaction, self.sprite,
                                            self.partner, self.hierarchy).actions

    # -------------------------------------------------------------------------

    def get_level_predicates(self):
        pass

    # -------------------------------------------------------------------------

    def get_methods(self):
        self.methods  = InteractionMethods(self.interaction, self.sprite,
                                            self.partner, self.hierarchy).methods

    # -------------------------------------------------------------------------

    def get_predicates(self):
        pass

    # -------------------------------------------------------------------------

    def get_task(self):
        pass
 
###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class InteractionMethods:
    """ Returns a method depending of the interaction """
    def __init__(self, interaction, sprite, partner, hierarchy):
        self.interaction = interaction
        self.sprite      = sprite
        self.partner     = partner
        
        self.methods = []
        self.get_methods()

    def get_methods(self):
        """ Return a method depending of the interaction """

        # [GVGAI] Adds a certain quantity of health points
        if self.interaction.type == "addHealthPoints":
            self.methods.append(addHealthPoints())

        # [GVGAI] Puts health points to max
        if self.interaction.type == "addHealthPointsToMax":
            self.methods.append(addHealthPointsToMax())

        # [GVGAI] Changes position and orientation of sprite to partner
        if self.interaction.type == "align":
            self.methods.append(align())

        # Randomly changesdirection of partner
        if self.interaction.type == "attractGaze":
            self.methods.append(attractGaze())

        # Not sure what it does, seems like the center of the object decides the direction
        if self.interaction.type == "bounceDirection":
            self.methods.append(bounceDirection())

        # Sprite tries to move in the opposite direction of partner
        if self.interaction.type == "bounceForward":
            self.methods.append(bounceForward())

        # Change resource (sprite) in the object (partner) to a given
        if self.interaction.type == "changeResource":
            self.methods.append(changeResource())

        # Creates a copy
        if self.interaction.type == "cloneSprite":
            self.methods.append(cloneSprite())

        # Increment resource (sprite) in the object (partner)
        if self.interaction.type == "collectResource":
            self.methods.append(collectResource())

        # [GVGAI] Decrease speed of all objects of the type of the sprite
        if self.interaction.type == "decreaseSpeedToAll":
            self.methods.append(decreaseSpeedToAll())

        # Changes to a random orientation
        if self.interaction.type == "flipDirection":
            self.methods.append(flipDirection())

        # [GVGAI] Increase speed of all objects of the sprite type
        if self.interaction.type == "increaseSpeedToAll":
            self.methods.append(increaseSpeedToAll())

        # [GVGAI] Kill all sprite of the same type
        if self.interaction.type == "killAll":
            self.methods.append(killAll())

        # Sprite and partner dies
        if self.interaction.type == "killBoth":
            self.methods.append(killBoth())

        # Kill sprite if partner is not destroyed by the collision
        if self.interaction.type == "killIfAlive":
            self.methods.append(killIfAlive())

        # Kill sprite if partner is above him
        if self.interaction.type == "killIfFromAbove":
            self.methods.append(killIfFromAbove())

        # If sprite has more resource than parameter (limit), kill it
        if self.interaction.type == "killIfHasMore":
            self.methods.append(killIfHasMore())

        # Not found in the GVGAI files
        # If sprite has less resource than parameter (limit), kill it
        # if self.interaction.type == "killIfHasLess":
            # pass    

        # Kill sprite if speed is higher than the given
        if self.interaction.type == "killIfFast":
            self.methods.append(killIfFast())

        # If partner has less resource than parameter (limit), kill sprite
        if self.interaction.type == "killIfOtherHasLess":
            self.methods.append(killIfOtherHasLess())

        # If partner has more resource than parameter (limit), kill sprite
        if self.interaction.type == "killIfOtherHasMore":
            self.methods.append(killIfOtherHasMore())

        # Kill sprite if speed is lower than the given
        if self.interaction.type == "killIfSlow":
            self.methods.append(killIfSlow())

        # Sprite dies
        if self.interaction.type == "killSprite":
            self.methods.append(killSprite())

        # Movement of partner is added to sprite (same quantity and direction)
        if self.interaction.type == "pullWithIt":
            self.methods.append(pullWithIt())

        # [GVGAI] Changes score of the avatar
        if self.interaction.type == "removeScore":
            self.methods.append(removeScore()) 

        # Changes orientation 180º
        if self.interaction.type == "reverseDirection":
            self.methods.append(reverseDirection())

        # [GVGAI] Asigns a specific speed to the sprite
        if self.interaction.type == "setSpeedToAll":
            self.methods.append(setSpeedToAll())

        # Creates sprite behind partner
        if self.interaction.type == "spawnBehind":
            self.methods.append(spawnBehind())

        # If sprite has less resource than parameter (limit), create new sprite
        if self.interaction.type == "spawnIfHasLess":
            self.methods.append(spawnIfHasLess())

        # If sprite has more resource than parameter (limit), create new sprite
        if self.interaction.type == "spawnIfHasMore":
            self.methods.append(spawnIfHasMore())

        # Undo last movement
        if self.interaction.type == "stepBack":
            self.methods.append(stepBack())

        # [GVGAI] Decrease a certain quantity of health points
        if self.interaction.type == "substractHealthPoints":
            self.methods.append(subsctractHealthPoints())

        # Move sprite to partner position (must be a Portal, if not, destroy sprite)
        if self.interaction.type == "teleportToExit":
            self.methods.append(teleportToExit())

        # [GVGAI] Changes sprite to stype if there are a certain quantity (stypeCount)
        if self.interaction.type == "transformIfCount":
            self.methods.append(transformIfCounts())

        # Seems like it creates a new copy of sprite
        if self.interaction.type == "transformTo":
            self.methods.append(transformTo())

        # [GVGAI] Transform sprite to one of his childs
        if self.interaction.type == "transformToRandomChild":
            self.methods.append(transformToRandomChild())

        # [GVGAI] Transform all sprites of stype to stype_other in the same position
        if self.interaction.type == "transformToSingleton":
            self.methods.append(transformToSingleton())

        # Not sure what it does, in VGDL seems to call reverseDirection
        if self.interaction.type == "turnAround":
            self.methods.append(turnAround())

        # Undo movement of every object in the game
        if self.interaction.type == "undoAll":
            self.methods.append(undoAll())

        # [GVGAI] Changes the "spawn type" to SpawnPoint
        if self.interaction.type == "updateSpawnType":
            self.methods.append(updateSpawnType())

        # Bounce in a perpendicular direction from the wall
        if self.interaction.type == "wallBounce":
            self.methods.append(wallBounce())

        # Stops sprite in front of wall
        if self.interaction.type == "wallStop":
            self.methods.append(wallStop())

        # Move sprite at the end of the screen in the orientation of sprite
        if self.interaction.type == "wrapAround":
            self.methods.append(wrapAround())

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    # UNFINISHED
    def addHealthPoints(self):        
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_addhealthpoints"
        # preconditions = ["(evaluate-interaction " + self.sprite.name + " - " +
        #                     self.sprite.stype + " " + self.partner.name + " - " +
        #                     self.partner.stype + ")"],
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_ADDHEALTHPOINTS ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def addHealthPointsToMax(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_addhealthpointstomax"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_ADDHEALTHPOINTSTOMAX ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def align(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_align"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_ALIGN ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def attractGaze(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_attractgaze"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_ATTRACTGAZE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)       

    # -------------------------------------------------------------------------

    # UNFINISHED
    def bounceDirection(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_bouncedirection"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_BOUNCEDIRECTION ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def bounceForward(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_bounceforward"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_BOUNCEFORWARD ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def changeResource(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_changeresource"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_CHANGERESOURCE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def cloneSprite(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_clonesprite"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_CLONESPRITE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def collectResource(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_collectresource"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_COLLECTRESOURCE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def decreaseSpeedToAll(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_decreasespeedtoall"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_DECREASESPEEDTOALL ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def flipDirection(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_flipdirection"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_FLIPDIRECTION ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)  

    # -------------------------------------------------------------------------

    # UNFINISHED
    def increaseSpeedToAll(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_increasespeedtoall"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_INCREASESPEEDTOALL ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killAll(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_killall"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_KILLALL ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killBoth(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_killboth"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_KILLBOTH ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfAlive(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_killifalive"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_KILLIFALIVE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfFromAbove(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_killiffromabove"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_KILLIFFROMABOVE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfHasMore(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_killifhasmore"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_KILLIFHASMORE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfFast(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_killiffast"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_KILLIFFAST ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfOtherHasLess(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_killifotherhasless"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_KILLIFOTHERHASLESS ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    # NEEDED REST OF THE NAME
    def killIfOtherHasMore(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_killifotherhasmore"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_KILLIFOTHERHASMORE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killIfSlow(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_killifslow"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_KILLIFSLOW ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killSprite(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_killsprite"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_KILLSPRITE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def pullWithIt(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_pullwithit"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_PULLWITHIT ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def removeScore(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_removescore"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_REMOVESCORE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def reverseDirection(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_reversedirection"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_REVERSEDIRECTION ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def setSpeedToAll(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_setspeedtoall"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_SETSPEEDTOALL ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def spawnBehind(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_spawnbehind"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_SPAWNBEHIND ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def spawnIfHasLess(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_spawnifhasless"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_SPAWNIFHASLESS ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def spawnIfHasMore(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_spawnifhasmore"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_SPAWNIFHASMORE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def stepBack(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_stepback"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_STEPBACK ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def subsctractHealthPoints(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_substracthealthpoints"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_SUBSTRACTHEALTHPOINTS ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def teleportToExit(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_teleporttoexit"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_TELEPORTTOEXIT ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def transformIfCount(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_transformifcount"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_TRANSFORMIFCOUNT ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    # NEEDED REST OF THE NAME
    def transformTo(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_transformto"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_TRANSFORMTO ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def transformToRandomChild(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_transformtorandomchild"
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_TRANSFORMTORANDOMCHILD ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def transformToSingleton(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_transformtosingleton"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_TRANSFORMTOSINGLETON ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def turnAround(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_turnaround"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_TURNAROUND ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def undoAll(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_undoall"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_UNDOALL ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def updateSpawnType(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_updatespawntype"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_UPDATESPAWNTYPE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def wallBounce(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_wallbounce"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_WALLBOUNCE ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def wallStop(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_WALLSTOP"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_WALLSTOP ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def wrapAround(self):
        name = self.sprite.name.lower() + "_" + self.partner.name.lower() + "_wraparound"  
        preconditions = ["(evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")",
                         "(not (= (coordinate_x ?x) -1))",
                         "(not (= (coordinate_x ?y) -1))"]
        tasks         = ["(" + self.sprite.name.upper() + "_" 
                            + self.partner.name.upper() 
                            + "_WRAPAROUND ?x ?y)",
                        "(:inline () (not (evaluate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + ")))",
                        "(:inline () (regenerate-interaction ?x - " + self.sprite.stype + 
                            " " + "?y - " + self.partner.stype + "))",
                        "(check-interactions)"]

        return Method(name, preconditions, tasks)

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class InteractionActions:
    """ Returns an action for each interaction """
    def __init__(self, interaction, sprite, partner, hierarchy):
        self.interaction = interaction
        self.sprite      = sprite
        self.partner     = partner
        self.hierarchy    = hierarchy
        
        self.actions = []
        self.get_actions()

    def get_actions(self):
        """ Return an action depending of the interaction """
        # [GVGAI] Adds a certain quantity of health points
        if self.interaction.type == "addHealthPoints":
            self.actions.append(addHealthPoints())

        # [GVGAI] Puts health points to max
        if self.interaction.type == "addHealthPointsToMax":
            self.actions.append(addHealthPointsToMax())

        # [GVGAI] Changes position and orientation of sprite to partner
        if self.interaction.type == "align":
            self.actions.append(align())

        # Randomly changesdirection of partner
        if self.interaction.type == "attractGaze":
            self.actions.append(attractGaze())

        # Not sure what it does, seems like the center of the object decides the direction
        if self.interaction.type == "bounceDirection":
            self.actions.append(bounceDirection())

        # Sprite tries to move in the opposite direction of partner
        if self.interaction.type == "bounceForward":
            self.actions.append(bounceForward())

        # Change resource (sprite) in the object (partner) to a given
        if self.interaction.type == "changeResource":
            self.actions.append(changeResource())

        # Creates a copy
        if self.interaction.type == "cloneSprite":
            self.actions.append(cloneSprite())

        # Increment resource (sprite) in the object (partner)
        if self.interaction.type == "collectResource":
            self.actions.append(collectResource())

        # [GVGAI] Decrease speed of all objects of the type of the sprite
        if self.interaction.type == "decreaseSpeedToAll":
            self.actions.append(decreaseSpeedToAll())

        # Changes to a random orientation
        if self.interaction.type == "flipDirection":
            self.actions.append(flipDirection())

        # [GVGAI] Increase speed of all objects of the sprite type
        if self.interaction.type == "increaseSpeedToAll":
            self.actions.append(increaseSpeedToAll())

        # [GVGAI] Kill all sprite of the same type
        if self.interaction.type == "killAll":
            self.actions.append(killAll())

        # Sprite and partner dies
        if self.interaction.type == "killBoth":
            self.actions.append(killBoth())

        # Kill sprite if partner is not destroyed by the collision
        if self.interaction.type == "killIfAlive":
            self.actions.append(killIfAlive())

        # Kill sprite if partner is above him
        if self.interaction.type == "killIfFromAbove":
            self.actions.append(killIfFromAbove())

        # If sprite has more resource than parameter (limit), kill it
        if self.interaction.type == "killIfHasMore":
            self.actions.append(killIfHasMore())

        # Not found in the GVGAI files
        # If sprite has less resource than parameter (limit), kill it
        # if self.interaction.type == "killIfHasLess":
            # pass    

        # Kill sprite if speed is higher than the given
        if self.interaction.type == "killIfFast":
            self.actions.append(killIfFast())

        # If partner has less resource than parameter (limit), kill sprite
        if self.interaction.type == "killIfOtherHasLess":
            self.actions.append(killIfOtherHasLess())

        # If partner has more resource than parameter (limit), kill sprite
        if self.interaction.type == "killIfOtherHasMore":
            self.actions.append(killIfOtherHasMore())

        # Kill sprite if speed is lower than the given
        if self.interaction.type == "killIfSlow":
            self.actions.append(killIfSlow())

        # Sprite dies
        if self.interaction.type == "killSprite":
            self.actions.append(killSprite())

        # Movement of partner is added to sprite (same quantity and direction)
        if self.interaction.type == "pullWithIt":
            self.actions.append(pullWithIt())

        # [GVGAI] Changes score of the avatar
        if self.interaction.type == "removeScore":
            self.actions.append(removeScore()) 

        # Changes orientation 180º
        if self.interaction.type == "reverseDirection":
            self.actions.append(reverseDirection())

        # [GVGAI] Asigns a specific speed to the sprite
        if self.interaction.type == "setSpeedToAll":
            self.actions.append(setSpeedToAll())

        # Creates sprite behind partner
        if self.interaction.type == "spawnBehind":
            self.actions.append(spawnBehind())

        # If sprite has less resource than parameter (limit), create new sprite
        if self.interaction.type == "spawnIfHasLess":
            self.actions.append(spawnIfHasLess())

        # If sprite has more resource than parameter (limit), create new sprite
        if self.interaction.type == "spawnIfHasMore":
            self.actions.append(spawnIfHasMore())

        # Undo last movement
        if self.interaction.type == "stepBack":
            self.actions.append(stepBack())

        # [GVGAI] Decrease a certain quantity of health points
        if self.interaction.type == "substractHealthPoints":
            self.actions.append(subsctractHealthPoints())

        # Move sprite to partner position (must be a Portal, if not, destroy sprite)
        if self.interaction.type == "teleportToExit":
            self.actions.append(teleportToExit())

        # [GVGAI] Changes sprite to stype if there are a certain quantity (stypeCount)
        if self.interaction.type == "transformIfCount":
            self.actions.append(transformIfCounts())

        # Seems like it creates a new copy of sprite
        if self.interaction.type == "transformTo":
            self.actions.append(transformTo())

        # [GVGAI] Transform sprite to one of his childs
        if self.interaction.type == "transformToRandomChild":
            self.actions.append(transformToRandomChild())

        # [GVGAI] Transform all sprites of stype to stype_other in the same position
        if self.interaction.type == "transformToSingleton":
            self.actions.append(transformToSingleton())

        # Not sure what it does, in VGDL seems to call reverseDirection
        if self.interaction.type == "turnAround":
            self.actions.append(turnAround())

        # Undo movement of every object in the game
        if self.interaction.type == "undoAll":
            self.actions.append(undoAll())

        # [GVGAI] Changes the "spawn type" to SpawnPoint
        if self.interaction.type == "updateSpawnType":
            self.actions.append(updateSpawnType())

        # Bounce in a perpendicular direction from the wall
        if self.interaction.type == "wallBounce":
            self.actions.append(wallBounce())

        # Stops sprite in front of wall
        if self.interaction.type == "wallStop":
            self.actions.append(wallStop())

        # Move sprite at the end of the screen in the orientation of sprite
        if self.interaction.type == "wrapAround":
            self.actions.append(wrapAround()))

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def addHealthPoints(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_ADDHEALTHPOINTS"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def addHealthPointsToMax(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_ADDHEALTHPOINTSTOMAX"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def align(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_ALIGN"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def attractGaze(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_ATTRACTGAZE"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def bounceDirection(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_BOUNCEDIRECTION"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def bounceForward(self):
        """ Move in the same direction of partner """
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_BOUNCEFORWARD"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = ["""
                        (when
                            (orientation-up ?y)

                            (and
                                (assign (last_coordinate_y ?x) (coordinate_y ?x))
                                (decrease (coordinate_y ?x) 1)
                            )
                        )
                        (when
                            (orientation-down ?y)

                            (and
                                (assign (last_coordinate_y ?x) (coordinate_y ?x))
                                (increase (coordinate_y ?x) 1)
                            )
                        )
                        (when
                            (orientation-left ?y)

                            (and
                                (assign (last_coordinate_x ?x) (coordinate_x ?x))
                                (decrease (coordinate_x ?x) 1)
                            )
                        )
                        (when
                            (orientation-right ?y)

                            (and
                                (assign (last_coordinate_x ?x) (coordinate_x ?x))
                                (increase (coordinate_x ?x) 1)
                            )
                        )"""]

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def changeResource(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_CHANGERESOURCE"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def cloneSprite(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_CLONESPRITE"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def collectResource(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_COLLECTRESOURCE"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = ["(assign (last_coordinate_y ?x) (coordinate_x ?x))",
					"(assign (last_coordinate_y ?x) (coordinate_y ?x))",
					"(assign (coordinate_x ?x) -1)",
					"(assign (coordinate_y ?x) -1)",
					"(decrease (counter_" + self.sprite.stype + ") 1)",
					"(decrease (counter_Resource) 1)",
					"(decrease (counter_Object) 1)",

					"(increase (resource_" + self.sprite.name + " ?a) 1)"]

        for parent in self.hierarchy[self.sprite.stype]:
            effects.append("(decrease (counter_" + parent + ") 1)")

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def decreaseSpeedToAll(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_INCREASESPEEDTOALL"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def flipDirection(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_FLIPDIRECTION"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def increaseSpeedToAll(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_INCREASESPEEDTOALL"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killAll(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_KILLALL"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killBoth(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_KILLBOTH"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = ["(assign (last_coordinate_x ?x) (coordinate_x ?x))",
                   "(assign (last_coordinate_y ?x) (coordinate_y ?x))",
                   "(assign (last_coordinate_x ?y) (coordinate_x ?y))",
                   "(assign (coordinate_x ?x) -1)",
                   "(assign (coordinate_y ?x) -1)",
                   "(assign (coordinate_x ?y) -1)",
                   "(assign (coordinate_y ?y) -1)",
                   "(decrease (counter_" + self.sprite.stype + ") 1)",                       
                   "(decrease (counter_" + self.partner.stype + ") 1)",
                   ]

        for parent in self.hierarchy[self.sprite.stype]:
            effects.append("(decrease (counter_" + parent + ") 1)")

        for parent in self.hierarchy[self.partner.stype]:
            effects.append("(decrease (counter_" + parent + ") 1)")

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfAlive(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_KILLIFALIVE"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------
    
    def killIfFromAbove(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_KILLIFFROMABOVE"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))",
                      "(= (last_coordinate_y ?y) (- (coordinate_y ?y) 1))"]
        effects = ["(assign (last_coordinate_y ?a) (coordinate_x ?a))",
					"(assign (last_coordinate_y ?a) (coordinate_y ?a))",
					"(assign (coordinate_x ?a) -1)",
					"(assign (coordinate_y ?a) -1)",
					"(decrease (counter_" + self.sprite.stype + ") 1)",
					"(decrease (counter_Object) 1)"]

        for parent in self.hierarchy[self.sprite.stype]:
            effects.append("(decrease (counter_" + parent + ") 1)")

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfHasMore(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_KILLIFHASMORE"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfFast(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_KILLIFFAST"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfOtherHasLess(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_KILLIFOTHERHASLESS"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfOtherHasMore(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_KILLIFOTHERHASMORE"
        # + self.third_sprite_type.upper() FIND TYPE IN PARAMETERS OF ACTION
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def killIfSlow(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_KILLIFSLOW"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def killSprite(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_KILLSPRITE"        
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [ "(assign (last_coordinate_y ?x) (coordinate_x ?x))",
					"(assign (last_coordinate_y ?x) (coordinate_y ?x))",
					"(assign (coordinate_x ?x) -1)",
					"(assign (coordinate_y ?x) -1)",

					"(decrease (counter_" + self.sprite.stype + ") 1)",					
					"(decrease (counter_Object) 1)"]

        for parent in self.hierarchy[self.sprite.stype]:
            effects.append("(decrease (counter_" + parent + ") 1)")

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def pullWithIt(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_PULLWITHIT"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def removeScore(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_REMOVESCORE"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def reverseDirection(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_REVERSEDIRECTION"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def setSpeedToAll(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_SETSPEEDTOALL"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def spawnBehind(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_SPAWNBEHING"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def spawnIfHasLess(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_SPAWNIFHASLESS"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def spawnIfHasMore(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_SPAWNIFHASMORE"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # Finished
    def stepBack(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_STEPBACK"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = ["(assign (coordinate_x ?x) (last_coordinate_x ?x))",
					"(assign (coordinate_y ?x) (last_coordinate_y ?x))"]

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def subsctractHealthPoints(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_SUBSCTRACTHEALTHPOINTS"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def teleportToExit(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_TELEPORTTOEXIT"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def transformIfCount(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_TRANSFORMIFCOUNT"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    # UNFINISHED
    def transformTo(self):
        # Find object to tranform
        # third_sprite = 

        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_TRANSFORMTO"
                # + self.third_sprite_type.upper() FIND TYPE IN PARAMETERS OF ACTION
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]#, ["z", third_sprite_type]]
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        
        effects = ["(assign (last_coordinate_x ?x) (coordinate_x ?x))",
                   "(assign (last_coordinate_y ?x) (coordinate_y ?x))",
                   "(assign (last_coordinate_x ?y) (coordinate_x ?y))",
                   "(assign (coordinate_x ?x) -1)",
                   "(assign (coordinate_y ?x) -1)",
                   "(assign (coordinate_x ?y) -1)",
                   "(assign (coordinate_y ?y) -1)",
                   "(decrease (counter_" + self.sprite.stype + ") 1)",                       
                   "(decrease (counter_" + self.partner.stype + ") 1)",

                    # Last coordinate is -1, no need to assign (is non-existen object)
                   "(assign (coordinate_x ?z) (last_coordinate_x ?x))",
                   "(assign (coordinate_y ?z) (last_coordinate_y ?x))"
                #    "(increase (counter_" + third_sprite_type + ") 1)"
                   ]

        for parent in self.hierarchy[self.sprite.stype]:
            effects.append("(decrease (counter_" + parent + ") 1)")

        for parent in self.hierarchy[self.partner.stype]:
            effects.append("(decrease (counter_" + parent + ") 1)")

        # for parent in self.hierarchy[self.third_sprite_type]:
        #     effects.append("(increase (counter_" + parent + ") 1)")

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def transformToRandomChild(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_TRANSFORMTORANDOMCHILD"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def transformToSingleton(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_TRANSFORMTOSINGLETON"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def turnAround(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_TURNAROUND"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def undoAll(self):
        """ This action always fail to force another movement"""
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_UNDOALL"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))",
                      "(not (= (coordinate_y ?x) (coordinate_y ?y)))"]
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def updateSpawnType(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_UPDATESPAWNTYPE"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def wallBounce(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_WALLBOUNCE"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def wallStop(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_WALLSTOP"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def wrapAround(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_WRAPAROUND"
        parameters = [["x", self.sprite.name], ["y", self.partner.stype]]       
        conditions = ["(= (coordinate_x ?x) (coordinate_x ?y))",
                      "(= (coordinate_y ?x) (coordinate_y ?y))"]
        effects = [] # UNFINISHED

        return Action(name, parameters, conditions, effects)