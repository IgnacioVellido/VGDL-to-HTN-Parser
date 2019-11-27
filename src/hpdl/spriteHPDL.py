###############################################################################
# sprite.py
# Ignacio Vellido Expósito
# 09/09/2019
# 
# Multiple classes defining parts of a HPDL domain for a non-avatar sprite
###############################################################################

from hpdl.hpdlTypes import *

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class SpriteHPDL:
    def __init__(self, sprite, hierarchy, partner=None):
        self.sprite = sprite
        self.hierarchy = hierarchy
        self.partner   = partner

        self.tasks              = []        
        self.methods            = []
        self.actions            = []
        self.predicates         = []
        self.level_predicates   = []

        get_actions()
        get_methods()
        get_tasks()
        get_predicates()
        get_level_predicates()

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def get_actions(self):
        spActions = SpriteActions(self.sprite, self.partner)
        self.actions = spActions.actions

    # -------------------------------------------------------------------------

    def get_level_predicates(self):
        pass

    # -------------------------------------------------------------------------

    def get_methods(self):
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

    def get_predicates(self):
        pass

    # -------------------------------------------------------------------------

    def get_tasks(self):
        pass


###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class SpriteActions:
    """ Return actions depending of the sprite (not including avatars) 
    
    These actions define the movements of the sprite not (directly) related with 
    interactions
    """
    def __init__(self, sprite, hierarchy, partner):
        self.sprite    = sprite
        self.hierarchy = hierarchy
        self.partner   = partner

        self.actions = []
        get_actions()

    # -------------------------------------------------------------------------

    def get_actions(self):
        # Not clear what it does
        # Missile that produces sprite at a specific ratio
        if self.sprite.stype == "Bomber":    
            self.actions.apend(self.produce())        
            # self.actions.apend(self.move(direction ??))
            pass

        # Follows partner (or avatar ?) sprite
        if self.sprite.stype == "Chaser":    
            # self.actions.apend(self.follow(partner))        
            pass

        # Missile that randomly changes direction
        if self.sprite.stype == "ErraticMissile":     
            # self.actions.apend(self.move(direction ??))                   
            # self.actions.apend(self.changeDirection()) - DOESN'T MAKE SENSE TO BE AN ACTION, IT'S RANDOM
            pass

        # Try to make the greatest distance with the partner (or avatar) sprite
        if self.sprite.stype == "Fleeing":       
            # self.actions.apend(self.flee(partner))     
            pass

        # Maybe not needed here
        # sprite that dissapear after a moment
        if self.sprite.stype == "Flicker":
            # self.actions.apend(self.disappear())
            pass

        # sprite that moves constantly in one direction
        if self.sprite.stype == "Missile":    
            self.actions.apend(self.move())

        # Maybe not needed here
        # Oriented sprite that dissapear after a moment
        if self.sprite.stype == "OrientedFlicker":            
            # self.actions.apend(self.dissapear())
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
            self.actions.apend(self.produce())

        # Expands in 4 directions if not occupied
        if self.sprite.stype == "Spreader":       
            # self.actions.apend(self.expand())     
            pass

        # Missile that if when it collides it change to a random direction
        if self.sprite.stype == "Walker":
            # self.actions.apend(self.move(direction ??))
            # If collides stop calculating until we know the new direction
            pass

        # Not clear what it does
        if self.sprite.stype == "WalkerJumper":            
            pass       

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    # def move(self, direction):
    def move(self):
        """ Move the sprite one position in the specified direction """
        name = self.sprite.name.upper() + "_MOVE"       
        parameters = []
        conditions = []
        effects = ["""
                    forall (?m - """ + self.sprite.stype + """)
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
"""]

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

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

    # UNFINISHED
    def produce(self):
        """ Generate an sprite - IN WICH POSITION ?? Down ?? 
        It should depend of the partner orientation <-
        """
        name = self.sprite.name.upper() + "_PRODUCE"
        # parameters = [["s", self.sprite.stype], ["p", self.partner.name]]        
        parameters = []
        # No need to check is position is available, if it is a wall (or 
        # something similar) the partner last position will be -1
        conditions = []

        # If no type is defined, get the parents name - MUST BE NEEDED LATER, ADD TO SPRITE sprite
        partner_stype = self.partner.father if self.partner.stype is None else self.partner.stype
        
        effects = ["""
                    forall (?s - """ + self.sprite.stype + 
                        """ ?p - """ + partner_stype + """)
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
"""]            

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def dissapear(self):
        """ Eliminates the sprite """
        pass

        name = self.sprite.name.upper() + "_DISSAPEAR"
        parameters = [["s", self.sprite.stype]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

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

# PROBABLY THE DOMAIN WILL ONLY NEED THE NAME OF THE ACTION, SO NO METHODS NEEDED
# class SpriteMethods:
#     """ Return methods depending of the sprite (not including avatars) """

#     def __init__(self, sprite.name, sprite.stype):
#         self.sprite.name = sprite.name
#         self.sprite.stype = sprite.stype

#     # -------------------------------------------------------------------------

#     def get_methods(self):
#         methods = []

#         # Not clear what it does
#         # Missile that produces sprite at a specific ratio
#         if self.sprite.stype == "Bomber":    
#             # methods.append(self.produce(partner))        
#             # methods.append(self.move(direction ??))
#             pass

#         # Follows partner (or avatar ?) sprite
#         if self.sprite.stype == "Chaser":    
#             # methods.append(self.follow(partner))        
#             pass

#         # Missile that randomly changes direction
#         if self.sprite.stype == "ErraticMissile":     
#             # methods.append(self.move(direction ??))                   
#             # methods.append(self.changeDirection()) - DOESN'T MAKE SENSE TO BE AN method, IT'S RANDOM
#             pass

#         # Try to make the greatest distance with the partner (or avatar) sprite
#         if self.sprite.stype == "Fleeing":       
#             # methods.append(self.flee(partner))     
#             pass

#         # Maybe not needed here
#         # sprite that dissapear after a moment
#         if self.sprite.stype == "Flicker":
#             # methods.append(self.disappear())
#             pass

#         # sprite that moves constantly in one direction
#         if self.sprite.stype == "Missile":          
#             # methods.append(self.move(direction ??))              
#             pass

#         # Maybe not needed here
#         # Oriented sprite that dissapear after a moment
#         if self.sprite.stype == "OrientedFlicker":            
#             # methods.append(self.dissapear())
#             pass

#         # Acts like a Chaser but sometimes it makes a random move
#         if self.sprite.stype == "RandomAltChaser":  
#             # The same methods that Chaser, random moves don't need to be defined
#             pass
        
#         # Acts like a Bomber but randomly change direction
#         if self.sprite.stype == "RandomBomber":            
#             # The same methods that Bomber, random moves don't need to be defined
#             pass

#         # Acts like a Missile but randomly change direction
#         if self.sprite.stype == "RandomMissile":            
#             # The same methods that Missile, random moves don't need to be defined
#             pass

#         # Chooses randomly an method in each iteration
#         if self.sprite.stype == "RandomNPC":         
#             # We can't know wich method will he choose, probably this will be empty  
#             # In case we want to add something, we should add each method of the NPC 
#             pass

#         # Produces sprites following a specific ratio
#         if self.sprite.stype == "SpawnPoint":  
#             # methods.append(self.produce(partner))          
#             pass

#         # Expands in 4 directions if not occupied
#         if self.sprite.stype == "Spreader":       
#             # methods.append(self.expand())     
#             pass

#         # Missile that if when it collides it change to a random direction
#         if self.sprite.stype == "Walker":
#             # methods.append(self.move(direction ??))
#             # If collides stop calculating until we know the new direction
#             pass

#         # Not clear what it does
#         if self.sprite.stype == "WalkerJumper":            
#             pass

       
#         return methods

#     # -------------------------------------------------------------------------
#     # -------------------------------------------------------------------------

    # def move(self, direction):
    #     name = self.sprite.name + "_MOVE"
    #     preconditions = []
    #     actions = ["(" + self.sprite.name + "_MOVE ?s ?p)"]    
        
    #     return Method(name, preconditions, actions)

#     # -------------------------------------------------------------------------

#     def expand(self):
#         name = self.sprite.name + "_EXPAND"
#         preconditions = []
#         actions = ["(" + self.sprite.name + "_EXPAND ?s ?p)"]    
        
#         return Method(name, preconditions, actions)
    
#     # -------------------------------------------------------------------------

#     def produce(self, partner):        
#         name = self.sprite.name + "_PRODUCE"
#         preconditions = []
#         actions = ["(" + self.sprite.name + "_PRODUCE ?s ?p)"]    
        
#         return Method(name, preconditions, actions)

#     # -------------------------------------------------------------------------

#     def dissapear(self):
#         name = self.sprite.name + "_DISSAPEAR"
#         preconditions = []
#         actions = ["(" + self.sprite.name + "_DISSAPEAR ?s ?p)"]    
        
#         return Method(name, preconditions, actions)

#     # -------------------------------------------------------------------------

#     def chase(self, partner):
#         name = self.sprite.name + "_CHASE"
#         preconditions = []
#         actions = ["(" + self.sprite.name + "_CHASE ?s ?p)"]    
        
#         return Method(name, preconditions, actions)

#     # -------------------------------------------------------------------------

#     def flee(self, partner):
#         name = self.sprite.name + "_FLEE"
#         preconditions = []
#         actions = ["(" + self.sprite.name + "_FLEE ?s ?p)"]    
        
#         return Method(name, preconditions, actions)