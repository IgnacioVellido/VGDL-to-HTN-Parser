###############################################################################
# sprite.py
# Ignacio Vellido Expósito
# 28/09/2020
#
# Multiple classes defining parts of a PDDL domain for a non-avatar sprite
###############################################################################

from pddl.typesPDDL import *

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################


class SpritePDDL:
    def __init__(self, sprite: "Sprite", hierarchy: dict, partner: "Sprite" = None):
        self.sprite = sprite
        self.hierarchy = hierarchy
        self.partner = partner

        self.tasks = []     # Empty
        self.methods = []   # Empty
        self.actions = []
        self.predicates = []
        self.level_predicates = []

        self.get_actions()
        self.get_predicates()
        self.get_level_predicates()

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    def get_actions(self) -> list:
        self.actions = SpriteActions(self.sprite, self.hierarchy, self.partner).actions

    # --------------------------------------------------------------------------

    def get_level_predicates(self) -> list:
        self.level_predicates = SpriteLevelPredicates(self.sprite).level_predicates

    # -------------------------------------------------------------------------

    def get_predicates(self) -> list:
        self.predicates = SpritePredicates(self.sprite).predicates

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################


class SpriteActions:
    """ Return actions depending of the sprite (not including avatars) 
    
    These actions define the movements of the sprite not (directly) related with 
    interactions
    """

    def __init__(self, sprite: "Sprite", hierarchy: dict, partner: "Sprite"):
        self.sprite = sprite
        self.hierarchy = hierarchy
        self.partner = partner

        self.actions = []
        
        # Dict with the functions needed for each avatar
        sprite_action_list = {
            # Not clear what it does
            # Missile that produces sprite at a specific ratio
            "Bomber": [self.spawn, self.spawn_stop],

            # Follows partner (or avatar ?) sprite
            "Chaser": [],
                # follow(partner))

            # Missile that randomly changes direction
            "ErraticMissile": [],
                # move(random_direction))
                # changeDirection())

            # Try to make the greatest distance with the partner (or avatar) sprite
            "Fleeing": [],
                # flee(partner))

            # sprite that dissapear after a moment
            "Flicker": [self.disappear, self.disappear_stop],

            # Doesn't do anything
            "Immovable": [],

            # sprite that moves constantly in one direction
            "Missile": [self.move_up, self.move_down, self.move_left, self.move_right, self.move_stop],

            # Oriented sprite that dissapear after a moment
            "OrientedFlicker": [self.disappear, self.disappear_stop],

            # Acts like a Chaser but sometimes it makes a random move
            # The same actions that Chaser, random moves don't need to be defined
            "RandomAltChaser": [],

            # Acts like a Bomber but randomly change direction
            # The same actions that Bomber, random moves don't need to be defined
            "RandomBomber": [],

            # Acts like a Missile but randomly change direction
            # The same actions that Missile, random moves don't need to be defined
            "RandomMissile": [],

            # Chooses randomly an action in each iteration
            # We can't know wich action will he choose, probably this will be empty
            # In case we want to add something, we should add each action of the NPC
            "RandomNPC": [],            

            # Produces sprites following a specific ratio
            "SpawnPoint": [self.spawn, self.spawn_stop],

            # Expands in 4 directions if not occupied
            "Spreader": [],
                # expand())

            # Missile that if when it collides it change to a random direction
            "Walker": [],
                # move(direction ??))
                # If collides stop calculating until we know the new direction ?

            # Not clear what it does
            "WalkerJumper": []
        }

        self.get_actions(sprite_action_list.get(self.sprite.stype, []))

    # -------------------------------------------------------------------------

    def get_actions(self, action_list):
        """ Stores in self.actions the actions defined """
        for function in action_list:
            self.actions.append(function())
        

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
	
    def move_stop(self):
        """ To finish MOVE sprite turn """
        name = "STOP_" + self.sprite.name.upper() + "_MOVE"
        parameters = []
        preconditions = ["(turn-" + self.sprite.name + "-move)", 
            "(forall (?x - " + self.sprite.name + ") (or (object-dead ?x) (" + self.sprite.name + "-moved ?x)))"]

        # Para FD habría que cambiar esto y quitar el forall
        effects = ["(forall (?x - " + self.sprite.name + ") (not (" + self.sprite.name + "-moved ?x)))",
			        "(not (turn-" + self.sprite.name + "-move))",
			        "(finished-turn-" + self.sprite.name + "-move)"]

        return Action(name, parameters, preconditions, effects)

    def move_up(self):
        """ Move the sprite one position """
        name = self.sprite.name.upper() + "_MOVE_UP"
        parameters = [["x", self.sprite.name], ["c_actual", "cell"], ["c_last", "cell"], ["c_next", "cell"]]
        preconditions = ["(turn-" + self.sprite.name + "-move)", "(oriented-up ?x)", "(at ?c_actual ?x)", "(last-at ?c_last ?x)", "(connected-up ?c_actual ?c_next)"]
        effects = ["(not (last-at ?c_last ?x))",
                    "(last-at ?c_actual ?x)",
                    "(not (at ?c_actual ?x))",
                    "(at ?c_next ?x)",
                    "(" + self.sprite.name + "-moved ?x)"]

        return Action(name, parameters, preconditions, effects)

    def move_down(self):
        """ Move the sprite one position """
        name = self.sprite.name.upper() + "_MOVE_DOWN"
        parameters = [["x", self.sprite.name], ["c_actual", "cell"], ["c_last", "cell"], ["c_next", "cell"]]
        preconditions = ["(turn-" + self.sprite.name + "-move)", "(oriented-down ?x)", "(at ?c_actual ?x)", "(last-at ?c_last ?x)", "(connected-down ?c_actual ?c_next)"]
        effects = ["(not (last-at ?c_last ?x))",
                    "(last-at ?c_actual ?x)",
                    "(not (at ?c_actual ?x))",
                    "(at ?c_next ?x)",
                    "(" + self.sprite.name + "-moved ?x)"]

        return Action(name, parameters, preconditions, effects)

    def move_left(self):
        """ Move the sprite one position """
        name = self.sprite.name.upper() + "_MOVE_LEFT"
        parameters = [["x", self.sprite.name], ["c_actual", "cell"], ["c_last", "cell"], ["c_next", "cell"]]
        preconditions = ["(turn-" + self.sprite.name + "-move)", "(oriented-left ?x)", "(at ?c_actual ?x)", "(last-at ?c_last ?x)", "(connected-left ?c_actual ?c_next)"]
        effects = ["(not (last-at ?c_last ?x))",
                    "(last-at ?c_actual ?x)",
                    "(not (at ?c_actual ?x))",
                    "(at ?c_next ?x)",
                    "(" + self.sprite.name + "-moved ?x)"]

        return Action(name, parameters, preconditions, effects)

    def move_right(self):
        """ Move the sprite one position """
        name = self.sprite.name.upper() + "_MOVE_RIGHT"
        parameters = [["x", self.sprite.name], ["c_actual", "cell"], ["c_last", "cell"], ["c_next", "cell"]]
        preconditions = ["(turn-" + self.sprite.name + "-move)", "(oriented-right ?x)", "(at ?c_actual ?x)", "(last-at ?c_last ?x)", "(connected-right ?c_actual ?c_next)"]
        effects = ["(not (last-at ?c_last ?x))",
                    "(last-at ?c_actual ?x)",
                    "(not (at ?c_actual ?x))",
                    "(at ?c_next ?x)",
                    "(" + self.sprite.name + "-moved ?x)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def expand(self):
        """ Expand all sprites in the 4 directions if unoccupied """
        # If no other sprite in that position...
        pass

        name = self.sprite.name.upper() + "_EXPAND"
        parameters = [["s", self.sprite.stype]]
        preconditions = []
        effects = []

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def spawn_stop(self):
        """ To finish SPAWN sprite turn """
        name = "STOP_" + self.sprite.name.upper() + "_SPAWN"
        parameters = []
        preconditions = ["(turn-" + self.sprite.name + "-spawn)", 
            "(forall (?x - " + self.sprite.name + ") (or (object-dead ?x) (" + self.sprite.name + "-spawned ?x)))"]

        # Para FD habría que cambiar esto y quitar el forall
        effects = ["(forall (?x - " + self.sprite.name + ") (not (" + self.sprite.name + "-spawned ?x)))",
			        "(not (turn-" + self.sprite.name + "-spawn))",
			        "(finished-turn-" + self.sprite.name + "-spawn)"]

        return Action(name, parameters, preconditions, effects)

    # WHAT ABOUT ORIENTATION ?
    # NOW IT IS PRODUCTION RATIO OF 1, BUT DIFFERS FROM GAME
    def spawn(self):
        """ Generate an sprite in the same cell """
        # Find object to spawn
        # If no type is defined, get the parents name
        spawned_object = (
            self.partner.father if self.partner.stype is None else self.partner.stype
        )

        name = self.sprite.name.upper() + "_SPAWN"
        parameters = [["x", self.sprite.name], ["y", spawned_object], ["c_actual", "cell"]]
        preconditions = [
            "(turn-" + self.sprite.name + "-spawn)",
            "(at ?c_actual ?x)",
            "(object-dead ?y)"
        ]
        effects = [
            "(not (object-dead ?y))",
            "(at ?c_actual ?y)",
            "(last-at ?c_actual ?y)"
            ""
        ]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    def disappear_stop(self):
        """ To finish DISAPPEAR sprite turn """
        name = "STOP_" + self.sprite.name.upper() + "_DISSAPEAR"
        parameters = []
        preconditions = ["(turn-" + self.sprite.name + "-disappear)", 
            "(forall (?x - " + self.sprite.name + ") (or (object-dead ?x) (" + self.sprite.name + "-disappeared ?x)))"]

        # Para FD habría que cambiar esto y quitar el forall
        effects = ["(forall (?x - " + self.sprite.name + ") (not (" + self.sprite.name + "-disappeared ?x)))",
			        "(not (turn-" + self.sprite.name + "-disappear))",
			        "(finished-turn-" + self.sprite.name + "-disappear)"]

        return Action(name, parameters, preconditions, effects)

    def disappear(self):
        """ Eliminates the sprite """
        name = self.sprite.name.upper() + "_DISAPPEAR"
        parameters = [["x", self.sprite.name], ["c_actual", "cell"]]
        preconditions = ["(turn-" + self.sprite.name + "-disappear)", "(at ?c_actual ?x)"]
        effects = ["(not (at ?c_actual ?x)", "(object-dead ?x)", "(" + self.sprite.name + "-disappeared ?x)"]

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def chase(self, partner):
        """ Choose the movement that moves toward the closest sprite of the 
        partner type """
        pass

        name = self.sprite.name.upper() + "_CHASE"
        parameters = [["s", self.sprite.stype], ["p", partner.name]]
        preconditions = []
        effects = []

        return Action(name, parameters, preconditions, effects)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def flee(self, partner):
        """ Choose the movement that moves away the closest sprite of the
        partner type """
        pass

        name = self.sprite.name.upper() + "_FLEE"
        parameters = [["s", self.sprite.stype], ["p", partner.name]]
        preconditions = []
        effects = []

        return Action(name, parameters, preconditions, effects)

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################


class SpritePredicates:
    """ Returns different predicates depending of the sprite """

    def __init__(self, sprite):
        self.sprite = sprite

        self.predicates = []
        self.get_predicates()

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def get_predicates(self):
        sprite_predicates_list = {
            # Not clear what it does
            # Missile that produces sprite at a specific ratio
            "Bomber": [
                "(" + self.sprite.name + "-spawned ?x - " + self.sprite.stype + ")",
                "(turn-" + self.sprite.name + "-spawn)",
                "(finished-turn-" + self.sprite.name + "-spawn)"
            ],

            # Follows partner (or avatar ?) sprite
            "Chaser": [],

            # Missile that randomly changes direction
            "ErraticMissile": [
                "(" + self.sprite.name + "-moved ?x - " + self.sprite.stype + ")",
                "(turn-" + self.sprite.name + "-move)",
                "(finished-turn-" + self.sprite.name + "-move)",
            ],

            # Try to make the greatest distance with the partner (or avatar) sprite
            "Fleeing": [],

            # Sprite that dissapear after a moment
            "Flicker": [
                "(" + self.sprite.name + "-disappeared ?x - " + self.sprite.stype + ")",
                "(turn-" + self.sprite.name + "-disappear)",
                "(finished-turn-" + self.sprite.name + "-disappear)",
            ],

            # Doesn't do anything
            "Immovable": [],

            # sprite that moves constantly in one direction
            "Missile": [
                "(" + self.sprite.name + "-moved ?x - " + self.sprite.stype + ")",
                # "(" + self.sprite.name + "-dead ?x - " + self.sprite.stype + ")",
                "(turn-" + self.sprite.name + "-move)",
                "(finished-turn-" + self.sprite.name + "-move)",
            ],

            # Maybe not needed here
            # Oriented sprite that dissapear after a moment
            "OrientedFlicker": [
                "(" + self.sprite.name + "-disappeared ?x - " + self.sprite.stype + ")",
                "(turn-" + self.sprite.name + "-disappear)",
                "(finished-turn-" + self.sprite.name + "-disappear)",
            ],                

            # Acts like a Chaser but sometimes it makes a random move
            # The same actions that Chaser, random moves don't need to be defined
            "RandomAltChaser": [],

            # Acts like a Bomber but randomly change direction
            # The same actions that Bomber, random moves don't need to be defined
            "RandomBomber": [],

            # Acts like a Missile but randomly change direction
            # The same actions that Missile, random moves don't need to be defined
            "RandomMissile": [],

            # Chooses randomly an action in each iteration
            # We can't know wich action will he choose, probably this will be empty
            # In case we want to add something, we should add each action of the NPC
            "RandomNPC": [],

            # Keep track of this object
            "Resource": ["(got-resource-" + self.sprite.name + " ?x - " + self.sprite.name + ")"],

            # Produces sprites following a specific ratio
            "SpawnPoint": [
                "(" + self.sprite.name + "-spawned ?x - " + self.sprite.stype + ")",
                "(turn-" + self.sprite.name + "-spawn)",
                "(finished-turn-" + self.sprite.name + "-spawn)"
            ],

            # Expands in 4 directions if not occupied
            "Spreader": [],

            # Missile that if when it collides it change to a random direction
            "Walker": [
                "(" + self.sprite.name + "-moved ?x - " + self.sprite.stype + ")",
                # "(" + self.sprite.name + "-dead ?x - " + self.sprite.stype + ")",
                "(turn-" + self.sprite.name + "-move)",
                "(finished-turn-" + self.sprite.name + "-move)",
            ],

            # Not clear what it does
            "WalkerJumper": []
        }

        # "FIX", but better try to include all keys manually if possible
        self.predicates.extend(sprite_predicates_list.get(self.sprite.stype, []))


###############################################################################
# -----------------------------------------------------------------------------
###############################################################################


class SpriteLevelPredicates:
    """ Returns different level predicates depending of the sprite """

    def __init__(self, sprite):
        self.sprite = sprite

        self.level_predicates = []
        self.get_level_predicates()

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def get_level_predicates(self):
        sprite_level_predicates_list = {
            # Not clear what it does
            # Missile that produces sprite at a specific ratio
            "Bomber": [],

            # Follows partner (or avatar ?) sprite
            "Chaser": [],

            # Missile that randomly changes direction
            "ErraticMissile": [self.get_orientation()],

            # Try to make the greatest distance with the partner (or avatar) sprite
            "Fleeing": [],

            # Maybe not needed here
            # sprite that dissapear after a moment
            "Flicker": [],

            # Doesn't do anything
            "Immovable": [],

            # sprite that moves constantly in one direction
            "Missile": [self.get_orientation()],

            # Maybe not needed here
            # Oriented sprite that dissapear after a moment
            "OrientedFlicker": [],
                # [self.dissapear()],

            # Acts like a Chaser but sometimes it makes a random move
            # The same actions that Chaser, random moves don't need to be defined
            "RandomAltChaser": [],

            # Acts like a Bomber but randomly change direction
            # The same actions that Bomber, random moves don't need to be defined
            "RandomBomber": [],

            # Acts like a Missile but randomly change direction
            # The same actions that Missile, random moves don't need to be defined
            "RandomMissile": [],

            # Chooses randomly an action in each iteration
            # We can't know wich action will he choose, probably this will be empty
            # In case we want to add something, we should add each action of the NPC
            "RandomNPC": [],

            # Produces sprites following a specific ratio
            "SpawnPoint": [],

            # Expands in 4 directions if not occupied
            "Spreader": [],

            # Missile that if when it collides it change to a random direction
            "Walker": [self.get_orientation()],

            # Not clear what it does
            "WalkerJumper": []
        }

        self.level_predicates.extend(sprite_level_predicates_list.get(self.sprite.stype, []))

    # -------------------------------------------------------------------------

    def get_orientation(self) -> str:
        orientation = [x for x in self.sprite.parameters if "oriented" in x]

        if len(orientation) > 1:
            orientation = orientation[0]
            orientation = orientation.split("=")[1]

            return "(oriented-" + orientation.lower() + " ?o)"
        else:
            return "(oriented-down ?o)"
