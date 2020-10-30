###############################################################################
# sprite.py
# Ignacio Vellido Expósito
# 09/09/2019
#
# Multiple classes defining parts of a HPDL domain for a non-avatar sprite
###############################################################################

from hpdl.typesHPDL import *

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################


class SpriteHPDL:
    def __init__(self, sprite: "Sprite", hierarchy: dict, partner: "Sprite" = None):
        self.sprite = sprite
        self.hierarchy = hierarchy
        self.partner = partner

        self.tasks = []
        self.methods = []
        self.actions = []
        self.predicates = []
        self.level_predicates = []

        self.get_actions()
        self.get_methods()
        self.get_tasks()
        self.get_predicates()
        self.get_level_predicates()

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    def get_actions(self) -> list:
        self.actions = SpriteActions(self.sprite, self.hierarchy, self.partner).actions

    # --------------------------------------------------------------------------

    def get_level_predicates(self) -> list:
        self.level_predicates = SpriteLevelPredicates(self.sprite).level_predicates

    # --------------------------------------------------------------------------

    def get_methods(self) -> list:
        for action in self.actions:
            name = action.name.upper()
            preconditions = []

            # Getting the parameters (only the name, not the type)
            parameters = ""
            for p in action.parameters:
                parameters += " ?" + p[0]

            m_action = "(" + action.name + parameters + ")"

            m = Method(name, preconditions, [m_action])

            self.methods.append(m)

    # -------------------------------------------------------------------------

    def get_predicates(self) -> list:
        pass

    # -------------------------------------------------------------------------

    def get_tasks(self) -> list:
        pass


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
        self.set_actions()

    # -------------------------------------------------------------------------

    def set_actions(self):
        """ Stores in self.actions the actions defined """
        # Not clear what it does
        # Missile that produces sprite at a specific ratio
        if self.sprite.stype == "Bomber":
            self.actions.append(self.produce())
            # self.actions.append(self.move(direction ??))
            pass

        # Follows partner (or avatar ?) sprite
        if self.sprite.stype == "Chaser":
            # self.actions.append(self.follow(partner))
            pass

        # Missile that randomly changes direction
        if self.sprite.stype == "ErraticMissile":
            # self.actions.append(self.move(direction ??))
            # self.actions.append(self.changeDirection()) - DOESN'T MAKE SENSE TO BE AN ACTION, IT'S RANDOM
            pass

        # Try to make the greatest distance with the partner (or avatar) sprite
        if self.sprite.stype == "Fleeing":
            # self.actions.append(self.flee(partner))
            pass

        # Maybe not needed here
        # sprite that dissapear after a moment
        if self.sprite.stype == "Flicker":
            # self.actions.append(self.disappear())
            pass

        # sprite that moves constantly in one direction
        if self.sprite.stype == "Missile":
            self.actions.append(self.move())

        # Maybe not needed here
        # Oriented sprite that dissapear after a moment
        if self.sprite.stype == "OrientedFlicker":
            # self.actions.append(self.disappear())
            pass

        # Acts like a Chaser but sometimes it makes a random move
        if self.sprite.stype == "RandomAltChaser":
            # The same actions that Chaser, random moves don't need to be defined
            pass

        # Acts like a Bomber but randomly change direction
        if self.sprite.stype == "RandomBomber":
            # The same actions that Bomber, random moves don't need to be defined
            pass

        # Acts like a Missile but randomly change direction
        if self.sprite.stype == "RandomMissile":
            # The same actions that Missile, random moves don't need to be defined
            pass

        # Chooses randomly an action in each iteration
        if self.sprite.stype == "RandomNPC":
            # We can't know wich action will he choose, probably this will be empty
            # In case we want to add something, we should add each action of the NPC
            pass

        # Produces sprites following a specific ratio
        if self.sprite.stype == "SpawnPoint":
            self.actions.append(self.produce())

        # Expands in 4 directions if not occupied
        if self.sprite.stype == "Spreader":
            # self.actions.append(self.expand())
            pass

        # Missile that if when it collides it change to a random direction
        if self.sprite.stype == "Walker":
            # self.actions.append(self.move(direction ??))
            # If collides stop calculating until we know the new direction
            pass

        # Not clear what it does
        if self.sprite.stype == "WalkerJumper":
            pass

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def move(self):
        """ Move the sprite one position """
        name = self.sprite.name.upper() + "_MOVE"
        parameters = []
        conditions = []
        effects = [
            """
                    forall (?m - """
            + self.sprite.stype
            + """)
					(and
						(when
							(orientation-up ?m)

							(and
								(assign (last_coordinate_y ?m) (coordinate_y ?m))
								(decrease (coordinate_y ?m) 1)						
							)
						)

						(when
							(orientation-down ?m)

							(and
								(assign (last_coordinate_y ?m) (coordinate_y ?m))
								(increase (coordinate_y ?m) 1)						
							)
						)

						(when
							(orientation-left ?m)

							(and
								(assign (last_coordinate_x ?m) (coordinate_x ?m))
								(decrease (coordinate_x ?m) 1)						
							)
						)

						(when
							(orientation-right ?m)

							(and
								(assign (last_coordinate_x ?m) (coordinate_x ?m))
								(increase (coordinate_x ?m) 1)			
							)
						)
					)
"""
        ]

        return Action(name, parameters, conditions, effects)

    # -------------------------------------------------------------------------

    # UNFINISHED
    def expand(self):
        """ Expand all sprites in the 4 directions if unoccupied """
        # If no other sprite in that position...
        pass

        name = self.sprite.name.upper() + "_EXPAND"
        parameters = [["s", self.sprite.stype]]
        conditions = []
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
        conditions = []

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
        conditions = []
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
        conditions = []
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
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)


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
        # Not clear what it does
        # Missile that produces sprite at a specific ratio
        if self.sprite.stype == "Bomber":
            pass

        # Follows partner (or avatar ?) sprite
        if self.sprite.stype == "Chaser":
            pass

        # Missile that randomly changes direction
        if self.sprite.stype == "ErraticMissile":
            self.level_predicates.append(self.get_orientation())

        # Try to make the greatest distance with the partner (or avatar) sprite
        if self.sprite.stype == "Fleeing":
            pass

        # Maybe not needed here
        # sprite that dissapear after a moment
        if self.sprite.stype == "Flicker":
            pass

        # sprite that moves constantly in one direction
        if self.sprite.stype == "Missile":
            self.level_predicates.append(self.get_orientation())

        # Maybe not needed here
        # Oriented sprite that dissapear after a moment
        if self.sprite.stype == "OrientedFlicker":
            # self.level_predicates.append(self.dissapear())
            pass

        # Acts like a Chaser but sometimes it makes a random move
        if self.sprite.stype == "RandomAltChaser":
            # The same actions that Chaser, random moves don't need to be defined
            pass

        # Acts like a Bomber but randomly change direction
        if self.sprite.stype == "RandomBomber":
            # The same actions that Bomber, random moves don't need to be defined
            pass

        # Acts like a Missile but randomly change direction
        if self.sprite.stype == "RandomMissile":
            # The same actions that Missile, random moves don't need to be defined
            pass

        # Chooses randomly an action in each iteration
        if self.sprite.stype == "RandomNPC":
            # We can't know wich action will he choose, probably this will be empty
            # In case we want to add something, we should add each action of the NPC
            pass

        # Produces sprites following a specific ratio
        if self.sprite.stype == "SpawnPoint":
            pass

        # Expands in 4 directions if not occupied
        if self.sprite.stype == "Spreader":
            pass

        # Missile that if when it collides it change to a random direction
        if self.sprite.stype == "Walker":
            # If collides stop calculating until we know the new direction
            self.level_predicates.append(self.get_orientation())

        # Not clear what it does
        if self.sprite.stype == "WalkerJumper":
            pass

    # -------------------------------------------------------------------------

    def get_orientation(self) -> str:
        orientation = [x for x in self.sprite.parameters if "orientation" in x]

        if len(orientation) > 0:
            orientation = orientation[0]
            orientation = orientation.split("=")[1]

            return "(orientation-" + orientation.lower() + " ?o)"
        else:
            return "(orientation-down ?o)"
