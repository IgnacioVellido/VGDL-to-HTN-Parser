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
            "Bomber": [produce],

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

            # Maybe not needed here
            # sprite that dissapear after a moment
            "Flicker": [],
                # disappear())

            # sprite that moves constantly in one direction
            "Missile": [move_up, move_down, move_left, move_right, move_stop],

            # Maybe not needed here
            # Oriented sprite that dissapear after a moment
            "OrientedFlicker": [],
                # [disappear]

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
            "SpawnPoint": [produce],

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

        # MAYBE NEEDS self BEFORE EACH FUNCTION
        get_actions(sprite_action_list[self.sprite.stype]())

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
        effects = ["(not (last-at ?c_last ?x))",
                    "(last-at ?c_actual ?x)",
                    "(not (at ?c_actual ?x))",
                    "(at ?c_next ?x)",
                    "(" + self.sprite.name + "-moved ?x)"]

        return Action(name, parameters, conditions, effects)

    def move_up(self):
        """ Move the sprite one position """
        name = self.sprite.name.upper() + "_MOVE_UP"
        parameters = ["(?x - " + self.sprite.name + " ?c_actual ?c_last ?c_next - cell)"]
        preconditions = ["(turn-" + self.sprite.name + "-move)", "(oriented-up ?x)", "(at ?f_actual ?x)", "(last-at ?c_last ?x)", "(connected-up ?c_actual ?c_next)"]
        effects = ["(forall (?x - " + self.sprite.name + ") (not (" + self.sprite.name + "-moved ?x)))",
			        "(not (turn-" + self.sprite.name + "-move))",
			        "(finished-turn-" + self.sprite.name + "-move)"]

        return Action(name, parameters, conditions, effects)

    def move_down(self):
        """ Move the sprite one position """
        name = self.sprite.name.downper() + "_MOVE_DOWN"
        parameters = ["(?x - " + self.sprite.name + " ?c_actual ?c_last ?c_next - cell)"]
        preconditions = ["(turn-" + self.sprite.name + "-move)", "(oriented-down ?x)", "(at ?f_actual ?x)", "(last-at ?c_last ?x)", "(connected-down ?c_actual ?c_next)"]
        effects = ["(forall (?x - " + self.sprite.name + ") (not (" + self.sprite.name + "-moved ?x)))",
			        "(not (turn-" + self.sprite.name + "-move))",
			        "(finished-turn-" + self.sprite.name + "-move)"]

        return Action(name, parameters, conditions, effects)

    def move_left(self):
        """ Move the sprite one position """
        name = self.sprite.name.leftper() + "_MOVE_LEFT"
        parameters = ["(?x - " + self.sprite.name + " ?c_actual ?c_last ?c_next - cell)"]
        preconditions = ["(turn-" + self.sprite.name + "-move)", "(oriented-left ?x)", "(at ?f_actual ?x)", "(last-at ?c_last ?x)", "(connected-left ?c_actual ?c_next)"]
        effects = ["(forall (?x - " + self.sprite.name + ") (not (" + self.sprite.name + "-moved ?x)))",
			        "(not (turn-" + self.sprite.name + "-move))",
			        "(finished-turn-" + self.sprite.name + "-move)"]

        return Action(name, parameters, conditions, effects)

    def move_right(self):
        """ Move the sprite one position """
        name = self.sprite.name.rightper() + "_MOVE_RIGHT"
        parameters = ["(?x - " + self.sprite.name + " ?c_actual ?c_last ?c_next - cell)"]
        preconditions = ["(turn-" + self.sprite.name + "-move)", "(oriented-right ?x)", "(at ?f_actual ?x)", "(last-at ?c_last ?x)", "(connected-right ?c_actual ?c_next)"]
        effects = ["(forall (?x - " + self.sprite.name + ") (not (" + self.sprite.name + "-moved ?x)))",
			        "(not (turn-" + self.sprite.name + "-move))",
			        "(finished-turn-" + self.sprite.name + "-move)"]

        return Action(name, parameters, conditions, effects)

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

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    # UNFINISHED -> INCREASE counters
    def produce(self):
        """ Generate an sprite - IN WICH POSITION ?? Down ?? 
        It should depend of the partner orientation <-
        """
        name = self.sprite.name.upper() + "_PRODUCE"
        parameters = []
        preconditions = []

        # If no type is defined, get the parents name
        partner_stype = (
            self.partner.father if self.partner.stype is None else self.partner.stype
        )

        effects = [
            """
                    forall (?s - """
            + self.sprite.stype
            + """ ?p - """
            + partner_stype
            + """)
					(and
                        (when
                            (= (coordinate_x ?p) -1)
                            (and                            
                                (assign (coordinate_x ?p) (coordinate_x ?s))
                                (assign (coordinate_y ?p) (coordinate_y ?s))
                                (increase (coordinate_y ?p) 1)
                            )                  
                        )
					)
"""
        ]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def disappear(self):
        """ Eliminates the sprite """
        pass

        name = self.sprite.name.upper() + "_DISAPPEAR"
        parameters = [["s", self.sprite.stype]]
        preconditions = []
        effects = []

        return Action(name, parameters, conditions, effects)

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

        return Action(name, parameters, conditions, effects)

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

        return Action(name, parameters, conditions, effects)

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
            "Bomber": [],

            # Follows partner (or avatar ?) sprite
            "Chaser": [],

            # Missile that randomly changes direction
            "ErraticMissile": [
                "(" + self.sprite.name + "-moved ?x - " + self.sprite.stype + ")",
                # "(" + self.sprite.name + "-dead ?x - " + self.sprite.stype + ")",
                "(turn-" + self.sprite.name + "-move)",
                "(finished-turn-" + self.sprite.name + "-move)",
            ],

            # Try to make the greatest distance with the partner (or avatar) sprite
            "Fleeing": [],

            # Maybe not needed here
            # sprite that dissapear after a moment
            "Flicker": [],

            # sprite that moves constantly in one direction
            "Missile": [
                "(" + self.sprite.name + "-moved ?x - " + self.sprite.stype + ")",
                # "(" + self.sprite.name + "-dead ?x - " + self.sprite.stype + ")",
                "(turn-" + self.sprite.name + "-move)",
                "(finished-turn-" + self.sprite.name + "-move)",
            ],

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
            "Walker": [
                "(" + self.sprite.name + "-moved ?x - " + self.sprite.stype + ")",
                # "(" + self.sprite.name + "-dead ?x - " + self.sprite.stype + ")",
                "(turn-" + self.sprite.name + "-move)",
                "(finished-turn-" + self.sprite.name + "-move)",
            ],

            # Not clear what it does
            "WalkerJumper": []
        }

        self.predicates.extend[sprite_predicates_list(self.sprite.stype)]


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

        self.level_predicates.extend[sprite_level_predicates_list(self.sprite.stype)]

    # -------------------------------------------------------------------------

    def get_orientation(self) -> str:
        orientation = [x for x in self.sprite.parameters if "oriented" in x]

        if len(orientation) > 1:
            orientation = orientation[0]
            orientation = orientation.split("=")[1]

            return "(oriented-" + orientation.lower() + " ?o)"
        else:
            return "(oriented-down ?o)"
