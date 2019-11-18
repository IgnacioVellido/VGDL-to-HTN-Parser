###############################################################################
# object.py
# Ignacio Vellido Expósito
# 09/09/2019
# 
# Multiple classes defining parts of a HPDL domain for a non-avatar object
###############################################################################

from hpdl.hpdlTypes import *

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class ObjectHPDL:
    def __init__(self, object_name, object_type, partner=None):
        self.object_name = object_name
        self.object_type = object_type

        self.actions    = ObjectActions(object_name, object_type, partner).get_actions()
        self.methods    = []
        self.get_methods()
        # self.tasks      = AvatarTasks(object_name, object_type, partner).tasks

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


###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class ObjectActions:
    """ Return actions depending of the sprite (not including avatars) 
    
    These actions define the movements of the sprite not (directly) related with 
    interactions
    """

    def __init__(self, object_name, object_type, partner):
        self.object_name = object_name
        self.object_type = object_type
        self.partner     = partner

    # -------------------------------------------------------------------------

    def get_actions(self):
        actions = []

        # Not clear what it does
        # Missile that produces object at a specific ratio
        if self.object_type == "Bomber":    
            actions.append(self.produce())        
            # actions.append(self.move(direction ??))
            pass

        # Follows partner (or avatar ?) object
        if self.object_type == "Chaser":    
            # actions.append(self.follow(partner))        
            pass

        # Missile that randomly changes direction
        if self.object_type == "ErraticMissile":     
            # actions.append(self.move(direction ??))                   
            # actions.append(self.changeDirection()) - DOESN'T MAKE SENSE TO BE AN ACTION, IT'S RANDOM
            pass

        # Try to make the greatest distance with the partner (or avatar) object
        if self.object_type == "Fleeing":       
            # actions.append(self.flee(partner))     
            pass

        # Maybe not needed here
        # Object that dissapear after a moment
        if self.object_type == "Flicker":
            # actions.append(self.disappear())
            pass

        # Object that moves constantly in one direction
        if self.object_type == "Missile":    
            actions.append(self.move())

        # Maybe not needed here
        # Oriented object that dissapear after a moment
        if self.object_type == "OrientedFlicker":            
            # actions.append(self.dissapear())
            pass

        # Acts like a Chaser but sometimes it makes a random move
        if self.object_type == "RandomAltChaser":  
            # The same actions that Chaser, random moves don't need to be defined
            pass
        
        # Acts like a Bomber but randomly change direction
        if self.object_type == "RandomBomber":            
            # The same actions that Bomber, random moves don't need to be defined
            pass

        # Acts like a Missile but randomly change direction
        if self.object_type == "RandomMissile":            
            # The same actions that Missile, random moves don't need to be defined
            pass

        # Chooses randomly an action in each iteration
        if self.object_type == "RandomNPC":         
            # We can't know wich action will he choose, probably this will be empty  
            # In case we want to add something, we should add each action of the NPC 
            pass

        # Produces objects following a specific ratio
        if self.object_type == "SpawnPoint":  
            actions.append(self.produce())

        # Expands in 4 directions if not occupied
        if self.object_type == "Spreader":       
            # actions.append(self.expand())     
            pass

        # Missile that if when it collides it change to a random direction
        if self.object_type == "Walker":
            # actions.append(self.move(direction ??))
            # If collides stop calculating until we know the new direction
            pass

        # Not clear what it does
        if self.object_type == "WalkerJumper":            
            pass
       
        return actions

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    # def move(self, direction):
    def move(self):
        """ Move the object one position in the specified direction """
        name = self.object_name.upper() + "_MOVE"       
        parameters = []
        conditions = []
        effects = ["""
                    forall (?m - """ + self.object_type + """)
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
        """ Expand all objects in the 4 directions if unoccupied """ 
        # If no other object in that position...
        pass

        name = self.object_name.upper() + "_EXPAND"
        parameters = [["s", self.object_type]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        
    
    # -------------------------------------------------------------------------

    # UNFINISHED
    def produce(self):
        """ Generate an object - IN WICH POSITION ?? Down ?? 
        It should depend of the partner orientation <-
        """
        name = self.object_name.upper() + "_PRODUCE"
        # parameters = [["s", self.object_type], ["p", self.partner.name]]        
        parameters = []
        # No need to check is position is available, if it is a wall (or 
        # something similar) the partner last position will be -1
        conditions = []

        # If no type is defined, get the parents name - MUST BE NEEDED LATER, ADD TO SPRITE OBJECT
        partner_stype = self.partner.father if self.partner.stype is None else self.partner.stype
        
        effects = ["""
                    forall (?s - """ + self.object_type + 
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
        """ Eliminates the object """
        pass

        name = self.object_name.upper() + "_DISSAPEAR"
        parameters = [["s", self.object_type]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def chase(self, partner):
        """ Choose the movement that moves toward the closest sprite of the 
        partner type """
        pass

        name = self.object_name.upper() + "_CHASE"
        parameters = [["s", self.object_type], ["p", partner.name]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def flee(self, partner):
        """ Choose the movement that moves away the closest sprite of the
        partner type """        
        pass

        name = self.object_name.upper() + "_FLEE"
        parameters = [["s", self.object_type], ["p", partner.name]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        


###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

# PROBABLY THE DOMAIN WILL ONLY NEED THE NAME OF THE ACTION, SO NO METHODS NEEDED
# class ObjectMethods:
#     """ Return methods depending of the sprite (not including avatars) """

#     def __init__(self, object_name, object_type):
#         self.object_name = object_name
#         self.object_type = object_type

#     # -------------------------------------------------------------------------

#     def get_methods(self):
#         methods = []

#         # Not clear what it does
#         # Missile that produces object at a specific ratio
#         if self.object_type == "Bomber":    
#             # methods.append(self.produce(partner))        
#             # methods.append(self.move(direction ??))
#             pass

#         # Follows partner (or avatar ?) object
#         if self.object_type == "Chaser":    
#             # methods.append(self.follow(partner))        
#             pass

#         # Missile that randomly changes direction
#         if self.object_type == "ErraticMissile":     
#             # methods.append(self.move(direction ??))                   
#             # methods.append(self.changeDirection()) - DOESN'T MAKE SENSE TO BE AN method, IT'S RANDOM
#             pass

#         # Try to make the greatest distance with the partner (or avatar) object
#         if self.object_type == "Fleeing":       
#             # methods.append(self.flee(partner))     
#             pass

#         # Maybe not needed here
#         # Object that dissapear after a moment
#         if self.object_type == "Flicker":
#             # methods.append(self.disappear())
#             pass

#         # Object that moves constantly in one direction
#         if self.object_type == "Missile":          
#             # methods.append(self.move(direction ??))              
#             pass

#         # Maybe not needed here
#         # Oriented object that dissapear after a moment
#         if self.object_type == "OrientedFlicker":            
#             # methods.append(self.dissapear())
#             pass

#         # Acts like a Chaser but sometimes it makes a random move
#         if self.object_type == "RandomAltChaser":  
#             # The same methods that Chaser, random moves don't need to be defined
#             pass
        
#         # Acts like a Bomber but randomly change direction
#         if self.object_type == "RandomBomber":            
#             # The same methods that Bomber, random moves don't need to be defined
#             pass

#         # Acts like a Missile but randomly change direction
#         if self.object_type == "RandomMissile":            
#             # The same methods that Missile, random moves don't need to be defined
#             pass

#         # Chooses randomly an method in each iteration
#         if self.object_type == "RandomNPC":         
#             # We can't know wich method will he choose, probably this will be empty  
#             # In case we want to add something, we should add each method of the NPC 
#             pass

#         # Produces objects following a specific ratio
#         if self.object_type == "SpawnPoint":  
#             # methods.append(self.produce(partner))          
#             pass

#         # Expands in 4 directions if not occupied
#         if self.object_type == "Spreader":       
#             # methods.append(self.expand())     
#             pass

#         # Missile that if when it collides it change to a random direction
#         if self.object_type == "Walker":
#             # methods.append(self.move(direction ??))
#             # If collides stop calculating until we know the new direction
#             pass

#         # Not clear what it does
#         if self.object_type == "WalkerJumper":            
#             pass

       
#         return methods

#     # -------------------------------------------------------------------------
#     # -------------------------------------------------------------------------

    # def move(self, direction):
    #     name = self.object_name + "_MOVE"
    #     preconditions = []
    #     actions = ["(" + self.object_name + "_MOVE ?s ?p)"]    
        
    #     return Method(name, preconditions, actions)

#     # -------------------------------------------------------------------------

#     def expand(self):
#         name = self.object_name + "_EXPAND"
#         preconditions = []
#         actions = ["(" + self.object_name + "_EXPAND ?s ?p)"]    
        
#         return Method(name, preconditions, actions)
    
#     # -------------------------------------------------------------------------

#     def produce(self, partner):        
#         name = self.object_name + "_PRODUCE"
#         preconditions = []
#         actions = ["(" + self.object_name + "_PRODUCE ?s ?p)"]    
        
#         return Method(name, preconditions, actions)

#     # -------------------------------------------------------------------------

#     def dissapear(self):
#         name = self.object_name + "_DISSAPEAR"
#         preconditions = []
#         actions = ["(" + self.object_name + "_DISSAPEAR ?s ?p)"]    
        
#         return Method(name, preconditions, actions)

#     # -------------------------------------------------------------------------

#     def chase(self, partner):
#         name = self.object_name + "_CHASE"
#         preconditions = []
#         actions = ["(" + self.object_name + "_CHASE ?s ?p)"]    
        
#         return Method(name, preconditions, actions)

#     # -------------------------------------------------------------------------

#     def flee(self, partner):
#         name = self.object_name + "_FLEE"
#         preconditions = []
#         actions = ["(" + self.object_name + "_FLEE ?s ?p)"]    
        
#         return Method(name, preconditions, actions)
