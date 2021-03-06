###############################################################################
# interaction.py
# Ignacio Vellido Expósito
# 28/09/2020
#
# Multiple classes defining parts of a PDDL domain for interactions
###############################################################################

from pddl.typesPDDL import *

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################


class InteractionPDDL:
    """ Class that encapsulate the generation of PDDL domain structures 
    for interactions 
    
    Attributes:
        interaction - InteractionVGDL
        sprite - Sprite
        partner - Sprite
        hierarchy - Dict<String,String>
    """

    def __init__(
        self,
        interaction: "Interaction",
        sprite: "Sprite",
        partner: "Sprite",
        hierarchy: dict,
    ):
        self.interaction = interaction
        self.sprite = sprite
        self.partner = partner
        self.hierarchy = hierarchy

        self.tasks = []     # Empty
        self.methods = []   # Empty
        self.actions = []
        self.predicates = []
        self.level_predicates = []

        self.get_actions()
        self.get_predicates()
        self.get_level_predicates()

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def get_actions(self):
        self.actions = InteractionActions(
            self.interaction, self.sprite, self.partner, self.hierarchy
        ).actions

    # -------------------------------------------------------------------------

    def get_level_predicates(self):
        pass

    # -------------------------------------------------------------------------

    def get_predicates(self):
        pass

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################


class InteractionActions:
    """ Returns an action for each interaction """

    def __init__(
        self,
        interaction: "Interaction",
        sprite: "Sprite",
        partner: "Sprite",
        hierarchy: dict,
    ):
        self.interaction = interaction
        self.sprite = sprite
        self.partner = partner
        self.hierarchy = hierarchy

        self.actions = []
        
        interaction_action_list = {
            # [GVGAI] Adds a certain quantity of health points
            "addHealthPoints":
                [self.addHealthPoints],

            # [GVGAI] Puts health points to max
            "addHealthPointsToMax":
                [self.addHealthPointsToMax],

            # [GVGAI] Changes position and orientation of sprite to partner
            "align":
                [self.align],

            # Randomly changesdirection of partner
            "attractGaze": [],
                # [self.attractGaze],

            # Not sure what it does, seems like the center of the object decides the direction
            "bounceDirection":
                [self.bounceDirection],

            # Sprite tries to move in the opposite direction of partner
            "bounceForward":
                [self.bounceForward_up, self.bounceForward_down, self.bounceForward_left, self.bounceForward_right],

            # Change resource (sprite) in the object (partner) to a given
            "changeResource":
                [self.changeResource],

            # Creates a copy
            "cloneSprite":
                [self.cloneSprite],

            # Increment resource (sprite) in the object (partner)
            "collectResource":
                [self.collectResource],

            # [GVGAI] Decrease speed of all objects of the type of the sprite
            "decreaseSpeedToAll":
                [self.decreaseSpeedToAll],

            # Changes to a random orientation
            "flipDirection":
                [self.flipDirection],

            # [GVGAI] Increase speed of all objects of the sprite type
            "increaseSpeedToAll":
                [self.increaseSpeedToAll],

            # [GVGAI] Kill all sprite of the same type
            "killAll":
                [self.killAll],

            # Sprite and partner dies
            "killBoth":
                [self.killBoth],

            # Kill sprite if partner is not destroyed by the collision
            "killIfAlive":
                [self.killIfAlive],

            # Kill sprite if partner is above him
            "killIfFromAbove":
                [self.killIfFromAbove],

            # If sprite has more resource than parameter (limit), kill it
            "killIfHasMore":
                [self.killIfHasMore],

            # If sprite has less resource than parameter (limit), kill it
            "killIfHasLess":
                [self.killIfHasLess],

            # Kill sprite if speed is higher than the given
            "killIfFast":
                [self.killIfFast],

            # If partner has less resource than parameter (limit), kill sprite
            "killIfOtherHasLess":
                [self.killIfOtherHasLess],

            # If partner has more resource than parameter (limit), kill sprite
            "killIfOtherHasMore":
                [self.killIfOtherHasMore],

            # Kill sprite if speed is lower than the given
            "killIfSlow":
                [self.killIfSlow],

            # Sprite dies
            "killSprite":
                [self.killSprite],

            # Movement of partner is added to sprite (same quantity and direction)
            "pullWithIt":
                [self.pullWithIt],

            # [GVGAI] Changes score of the avatar
            "removeScore":
                [self.removeScore],

            # Changes orientation 180º
            "reverseDirection":
                [self.reverseDirection],

            # [GVGAI] Asigns a specific speed to the sprite
            "setSpeedToAll":
                [self.setSpeedToAll],

            # Creates sprite behind partner
            "spawnBehind":
                [self.spawnBehind],

            # If sprite has less resource than parameter (limit), create new sprite
            "spawnIfHasLess":
                [self.spawnIfHasLess],

            # If sprite has more resource than parameter (limit), create new sprite
            "spawnIfHasMore":
                [self.spawnIfHasMore],

            # Undo last movement
            "stepBack":
                [self.stepBack],

            # [GVGAI] Decrease a certain quantity of health points
            "substractHealthPoints":
                [self.subsctractHealthPoints],

            # Move sprite to partner position (must be a Portal, if not, destroy sprite)
            "teleportToExit":
                [self.teleportToExit],

            # [GVGAI] Changes sprite to stype if there are a certain quantity (stypeCount)
            "transformIfCount":
                [self.transformIfCount],

            # Seems like it creates a new copy of sprite
            "transformTo":
                [self.transformTo],

            # [GVGAI] Transform sprite to one of his childs
            "transformToRandomChild":
                [self.transformToRandomChild],

            # [GVGAI] Transform all sprites of stype to stype_other in the same position
            "transformToSingleton":
                [self.transformToSingleton],

            # Invert orientation
            "turnAround":
                [self.turnAround],

            # Undo movement of every object in the game
            # FOR NOW, NOTHING
            "undoAll": 
                [],
                # [self.undoAll],

            # [GVGAI] Changes the "spawn type" to SpawnPoint
            "updateSpawnType":
                [self.updateSpawnType],

            # Bounce in a perpendicular direction from the wall
            "wallBounce":
                [self.wallBounce],

            # Stops sprite in front of wall
            "wallStop":
                [self.wallStop],

            # Move sprite at the end of the screen in the orientation of sprite
            "wrapAround":
                [self.wrapAround],
        }

        self.get_actions(interaction_action_list[self.interaction.type])

    def get_actions(self, action_list):
        """ Stores in self.actions the actions defined """
        for function in action_list:
            self.actions.append(function())

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def addHealthPoints(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_ADDHEALTHPOINTS"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def addHealthPointsToMax(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_ADDHEALTHPOINTSTOMAX"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def align(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_ALIGN"
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def attractGaze(self):
        name = (
            self.sprite.name.upper() + "_" + self.partner.name.upper() + "_ATTRACTGAZE"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def bounceDirection(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_BOUNCEDIRECTION"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def bounceForward_up(self):
        """ Move in the same direction of partner """
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_BOUNCEFORWARD_UP"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"], ["c_up", "cell"], ["c_last", "cell"]]
        preconditions = [
            "(turn-interactions)",
            "(not (= ?x ?y))",

            "(oriented-up ?y)",

            "(at ?c_actual ?x)",
            "(at ?c_actual ?y)",
            "(last-at ?c_last ?x)",

            "(connected-up ?c_actual ?c_up)"
        ]
        effects = [
            "(at ?c_up ?x)",
            "(not (at ?c_actual ?x))",
            "(not (at ?c_last ?x))",
            "(last-at ?c_actual ?x)"
        ]

        return Action(name, parameters, preconditions, effects)

    def bounceForward_down(self):
        """ Move in the same direction of partner """
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_BOUNCEFORWARD_DOWN"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"], ["c_down", "cell"], ["c_last", "cell"]]
        preconditions = [
            "(turn-interactions)",
            "(not (= ?x ?y))",

            "(oriented-down ?y)",

            "(at ?c_actual ?x)",
            "(at ?c_actual ?y)",
            "(last-at ?c_last ?x)",

            "(connected-down ?c_actual ?c_down)"
        ]
        effects = [
            "(at ?c_down ?x)",
            "(not (at ?c_actual ?x))",
            "(not (at ?c_last ?x))",
            "(last-at ?c_actual ?x)"
        ]

        return Action(name, parameters, preconditions, effects)

    def bounceForward_left(self):
        """ Move in the same direction of partner """
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_BOUNCEFORWARD_LEFT"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"], ["c_left", "cell"], ["c_last", "cell"]]
        preconditions = [
            "(turn-interactions)",
            "(not (= ?x ?y))",

            "(oriented-left ?y)",

            "(at ?c_actual ?x)",
            "(at ?c_actual ?y)",
            "(last-at ?c_last ?x)",

            "(connected-left ?c_actual ?c_left)"
        ]
        effects = [
            "(at ?c_left ?x)",
            "(not (at ?c_actual ?x))",
            "(not (at ?c_last ?x))",
            "(last-at ?c_actual ?x)"
        ]

        return Action(name, parameters, preconditions, effects)

    def bounceForward_right(self):
        """ Move in the same direction of partner """
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_BOUNCEFORWARD_RIGHT"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"], ["c_right", "cell"], ["c_last", "cell"]]
        preconditions = [
            "(turn-interactions)",
            "(not (= ?x ?y))",

            "(oriented-right ?y)",

            "(at ?c_actual ?x)",
            "(at ?c_actual ?y)",
            "(last-at ?c_last ?x)",

            "(connected-right ?c_actual ?c_right)"
        ]
        effects = [
            "(at ?c_right ?x)",
            "(not (at ?c_actual ?x))",
            "(not (at ?c_last ?x))",
            "(last-at ?c_actual ?x)"
        ]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def changeResource(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_CHANGERESOURCE"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # Clone sprite (partner dies by another interaction, carefull)
    def cloneSprite(self):
        name = (
            self.sprite.name.upper() + "_" + self.partner.name.upper() + "_CLONESPRITE"
        )
        # parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"], ["z", self.sprite.name]]
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"], ["z", self.sprite.name], ["c_last", "cell"]]
        preconditions = [
            "(turn-interactions)",
            "(not (= ?x ?y))",
            "(at ?c_actual ?x)",
            "(at ?c_actual ?y)",
            # If we remove this predicate it would be sent to a random cell ?
            # But we should be carefull with stepBack or undoAll
            "(at ?c_last x)",

            "(object-dead ?z)"
        ]
        effects = [
            "(not (object-dead ?z))",
            # This can generate infinite loops
            # "(at ?c_actual ?z)",
            # "(last-at ?c_actual ?z)"
            "(at ?c_last ?z)",
            "(last-at ?c_last ?z)"
        ]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def collectResource(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_COLLECTRESOURCE"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(turn-interactions)",
            "(not (= ?x ?y))",
            "(at ?c_actual ?x)",
            "(at ?c_actual ?y)"
        ]
        effects = [
            "(object-dead ?x)",
            "(got-resource-" + self.sprite.name + " ?x)"
        ]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def decreaseSpeedToAll(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_INCREASESPEEDTOALL"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def flipDirection(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_FLIPDIRECTION"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def increaseSpeedToAll(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_INCREASESPEEDTOALL"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def killAll(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_KILLALL"
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def killBoth(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_KILLBOTH"
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(turn-interactions)",
            "(not (= ?x ?y))",

            "(at ?c_actual ?x)",
            "(at ?c_actual ?y)"
        ]
        effects = [
            "(not (at ?c_actual ?x))",
            "(not (at ?c_actual ?y))",
            "(object-dead ?x)",
            "(object-dead ?y)"
        ]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def killIfAlive(self):
        name = (
            self.sprite.name.upper() + "_" + self.partner.name.upper() + "_KILLIFALIVE"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def killIfFromAbove(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_KILLIFFROMABOVE"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"], ["c_last", "cell"]]
        preconditions = [
            "(turn-interactions)",
            "(not (= ?x ?y))",

            "(at ?c_actual ?x)",
            "(at ?c_actual ?y)",

            "(last-at ?c_last ?y)",
            "(connected-up ?c_actual ?c_last)"
        ]
        effects = [
            "(not (at ?c_actual ?x))",
            "(object-dead ?x)",
        ]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # Kill sprite if sprite has more

    # ASSUMING SPRITE IS AN AVATAR, THE ACTION IS THE SAME AS KILLIFOTHERHASMORE
    def killIfHasMore(self):
        # Get resource name
        parameters = [p for p in self.interaction.parameters if "resource=" in p]
        resource = parameters[0].replace("resource=",'')

        # Get number needed
        parameters = [p for p in self.interaction.parameters if "limit=" in p]
        number = parameters[0].replace("limit=",'')
        number = int(number)

        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_KILLIFOTHERHASMORE"
        )
        
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(turn-interactions)",
            "(not (= ?x ?y))",
            "(at ?c_actual ?x)",
            "(at ?c_actual ?y)"
        ]

        effects = [
            "(object-dead ?x)"
        ]


        # Add number-sprites to parameters
        for i in range(number):
            parameters.append(["r" + str(i), resource])

        # Add number-preconditions
        for i in range(number):
            preconditions.append("(got-resource-" + resource + " ?r" + str(i) + ")")

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # Kill sprite if sprite has less
    def killIfHasLess(self):
        # Get resource name
        parameters = [p for p in self.interaction.parameters if "resource=" in p]
        resource = parameters[0].replace("resource=",'')

        # Get number needed
        parameters = [p for p in self.interaction.parameters if "limit=" in p]
        number = parameters[0].replace("limit=",'')
        number = int(number)

        name = (
            self.sprite.name.upper() + "_" + self.partner.name.upper()
            + "_KILLIFOTHERHASLESS"
        )
        
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(turn-interactions)",
            "(not (= ?x ?y))",
            "(at ?c_actual ?x)",
            "(at ?c_actual ?y)"
        ]

        effects = [
            "(object-dead ?x)"
        ]


        # Add number-sprites to parameters
        for i in range(number):
            parameters.append(["r" + str(i), resource])

        # Add number-preconditions
        for i in range(number):
            preconditions.append("(got-resource-" + resource + " ?r" + str(i) + ")")

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def killIfFast(self):
        name = (
            self.sprite.name.upper() + "_" + self.partner.name.upper() + "_KILLIFFAST"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def killIfOtherHasLess(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_KILLIFOTHERHASLESS"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # Other = partner
    # Kill sprite if partner has more

    # MAYBE NEED TO INCLUDE IN THE PREDICATE THE SECOND OBJECT
    # RIGHT NOW WE ARE MAKING THE ASSUMPTION THAT IT IS THE AVATAR
    def killIfOtherHasMore(self):
        # Get resource name
        parameters = [p for p in self.interaction.parameters if "resource=" in p]
        resource = parameters[0].replace("resource=",'')

        # Get number needed
        parameters = [p for p in self.interaction.parameters if "limit=" in p]
        number = parameters[0].replace("limit=",'')
        number = int(number)

        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_KILLIFOTHERHASMORE"
        )
        
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(turn-interactions)",
            "(not (= ?x ?y))",
            "(at ?c_actual ?x)",
            "(at ?c_actual ?y)"
        ]

        effects = [
            "(object-dead ?x)"
        ]


        # Add number-sprites to parameters
        for i in range(number):
            parameters.append(["r" + str(i), resource])

        # Add number-preconditions
        for i in range(number):
            preconditions.append("(got-resource-" + resource + " ?r" + str(i) + ")")

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def killIfSlow(self):
        name = (
            self.sprite.name.upper() + "_" + self.partner.name.upper() + "_KILLIFSLOW"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def killSprite(self):
        name = (
            self.sprite.name.upper() + "_" + self.partner.name.upper() + "_KILLSPRITE"
        )
        # partner.stype or partner.name ?
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]] 
        preconditions = [
            "(turn-interactions)",
            "(not (= ?x ?y))",

            "(at ?c_actual ?x)",
            "(at ?c_actual ?y)"
        ]
        effects = [
            "(not (at ?c_actual ?x))",
            "(object-dead ?x)"
        ]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def pullWithIt(self):
        name = (
            self.sprite.name.upper() + "_" + self.partner.name.upper() + "_PULLWITHIT"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def removeScore(self):
        name = (
            self.sprite.name.upper() + "_" + self.partner.name.upper() + "_REMOVESCORE"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def reverseDirection(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_REVERSEDIRECTION"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def setSpeedToAll(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_SETSPEEDTOALL"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def spawnBehind(self):
        name = (
            self.sprite.name.upper() + "_" + self.partner.name.upper() + "_SPAWNBEHING"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def spawnIfHasLess(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_SPAWNIFHASLESS"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def spawnIfHasMore(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_SPAWNIFHASMORE"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def stepBack(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_STEPBACK"
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"], ["c_last", "cell"]]
        preconditions = [
            "(turn-interactions)",
            "(not (= ?x ?y))",

            "(at ?c_actual ?x)",
            "(at ?c_actual ?y)",
            "(last-at ?c_last ?x)"
        ]
        effects = [
            "(not (at ?c_actual ?x))",
            "(at ?c_last ?x)"
        ]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def subsctractHealthPoints(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_SUBSCTRACTHEALTHPOINTS"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def teleportToExit(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_TELEPORTTOEXIT"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def transformIfCount(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_TRANSFORMIFCOUNT"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # Maintain orientation of the partner object
    def transformTo(self):
        # Find object to tranform
        parameters = [p for p in self.interaction.parameters if "stype=" in p]
        resulting_sprite = parameters[0].replace("stype=",'')

        name = (
            self.sprite.name.upper() + "_" + self.partner.name.upper() + "_TRANSFORMTO"
        )
        parameters = [
            ["x", self.sprite.name],
            ["y", self.partner.stype],
            ["z", resulting_sprite],
            ["c_actual", "cell"]
        ]
        preconditions = [
            "(turn-interactions)",
            "(not (= ?x ?y))",
            "(at ?c_actual ?x)",
            "(at ?c_actual ?y)",
            "(object-dead ?z)"
        ]

        effects = [
            "(not (at ?c_actual ?x))",
            # "(not (at ?c_actual ?y))",
            "(object-dead ?x)",
            # "(object-dead ?y)",
            "(at ?c_actual ?z)",
            "(last-at ?c_actual ?z)",
            "(not (object-dead ?z))",
            """(when
                        (oriented-up ?y)
                        (oriented-up ?z)
                    )
                    (when
                        (oriented-down ?y)
                        (oriented-down ?z)
                    )
                    (when
                        (oriented-left ?y)
                        (oriented-left ?z)
                    )
                    (when
                        (oriented-right ?y)
                        (oriented-right ?z)
                    )
            """
        ]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def transformToRandomChild(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_TRANSFORMTORANDOMCHILD"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def transformToSingleton(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_TRANSFORMTOSINGLETON"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # Invert orientation of sprite
    def turnAround(self):
        name = (
            self.sprite.name.upper() + "_" + self.partner.name.upper() + "_TURNAROUND"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(turn-interactions)",
            "(not (= ?x ?y))",
            "(at ?c_actual ?x)",
            "(at ?c_actual ?y)"
        ]
        effects = [
            "(when (oriented-up ?x) (and (not-oriented-up ?x) (oriented-down ?x))",
            "(when (oriented-down ?x) (and (not-oriented-down ?x) (oriented-up ?x))",
            "(when (oriented-left ?x) (and (not-oriented-left ?x) (oriented-right ?x))",
            "(when (oriented-right ?x) (and (not-oriented-right ?x) (oriented-left ?x))"
        ]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def undoAll(self):
        """ This action always fail to force another movement"""
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_UNDOALL"
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(turn-interactions)",
            "(not (= ?x ?y))",
            "(at ?c_actual ?x)",
            "(at ?c_actual ?y)"
        ]
        effects = ["(not (turn-interactions))"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def updateSpawnType(self):
        name = (
            self.sprite.name.upper()
            + "_"
            + self.partner.name.upper()
            + "_UPDATESPAWNTYPE"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def wallBounce(self):
        name = (
            self.sprite.name.upper() + "_" + self.partner.name.upper() + "_WALLBOUNCE"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def wallStop(self):
        name = self.sprite.name.upper() + "_" + self.partner.name.upper() + "_WALLSTOP"
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def wrapAround(self):
        name = (
            self.sprite.name.upper() + "_" + self.partner.name.upper() + "_WRAPAROUND"
        )
        parameters = [["x", self.sprite.name], ["y", self.partner.name], ["c_actual", "cell"]]
        preconditions = [
            "(= (coordinate_x ?x) (coordinate_x ?y))",
            "(= (coordinate_y ?x) (coordinate_y ?y))",
        ]
        effects = []  # UNFINISHED

        return Action(name, parameters, preconditions, effects)

