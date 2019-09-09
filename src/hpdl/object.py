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

class ObjectActions:
    """ Return actions depending of the sprite (not including avatars) 
    
    These actions define the movements of the sprite not (directly) related with 
    interactions
    """

    def __init__(self, sprite_name, sprite_type):
        self.sprite_name = sprite_name
        self.sprite_type = sprite_type

    # -------------------------------------------------------------------------

    def get_actions(self):
        actions = []

        # Not clear what it does
        # Missile that produces object at a specific ratio
        if self.sprite_type == "Bomber":    
            # actions.append(self.produce(partner))        
            # actions.append(self.move(direction ??))
            pass

        # Follows partner (or avatar ?) object
        if self.sprite_type == "Chaser":    
            # actions.append(self.follow(partner))        
            pass

        # Missile that randomly changes direction
        if self.sprite_type == "ErraticMissile":     
            # actions.append(self.move(direction ??))                   
            # actions.append(self.changeDirection()) - DOESN'T MAKE SENSE TO BE AN ACTION, IT'S RANDOM
            pass

        # Try to make the greatest distance with the partner (or avatar) object
        if self.sprite_type == "Fleeing":       
            # actions.append(self.flee(partner))     
            pass

        # Maybe not needed here
        # Object that dissapear after a moment
        if self.sprite_type == "Flicker":
            # actions.append(self.disappear())
            pass

        # Object that moves constantly in one direction
        if self.sprite_type == "Missile":          
            # actions.append(self.move(direction ??))              
            pass

        # Maybe not needed here
        # Oriented object that dissapear after a moment
        if self.sprite_type == "OrientedFlicker":            
            # actions.append(self.dissapear())
            pass

        # Acts like a Chaser but sometimes it makes a random move
        if self.sprite_type == "RandomAltChaser":  
            # The same actions that Chaser, random moves don't need to be defined
            pass
        
        # Acts like a Bomber but randomly change direction
        if self.sprite_type == "RandomBomber":            
            # The same actions that Bomber, random moves don't need to be defined
            pass

        # Acts like a Missile but randomly change direction
        if self.sprite_type == "RandomMissile":            
            # The same actions that Missile, random moves don't need to be defined
            pass

        # Chooses randomly an action in each iteration
        if self.sprite_type == "RandomNPC":         
            # We can't know wich action will he choose, probably this will be empty  
            # In case we want to add something, we should add each action of the NPC 
            pass

        # Produces objects following a specific ratio
        if self.sprite_type == "SpawnPoint":  
            # actions.append(self.produce(partner))          
            pass

        # Expands in 4 directions if not occupied
        if self.sprite_type == "Spreader":       
            # actions.append(self.expand())     
            pass

        # Missile that if when it collides it change to a random direction
        if self.sprite_type == "Walker":
            # actions.append(self.move(direction ??))
            # If collides stop calculating until we know the new direction
            pass

        # Not clear what it does
        if self.sprite_type == "WalkerJumper":            
            pass

       
        return actions

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def move(self, direction):
        """ Move the object one position in the specified direction """
        pass

        name = self.sprite_name + "_MOVE"
        parameters = [["s", self.sprite_type]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def expand(self):
        """ Expand all objects in the 4 directions if unoccupied """ 
        # If no other object in that position...
        pass

        name = self.sprite_name + "_EXPAND"
        parameters = [["s", self.sprite_type]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        
    
    # -------------------------------------------------------------------------

    def produce(self, partner):
        """ Generate an object - IN WICH POSITION ?? """
        pass

        name = self.sprite_name + "_PRODUCE"
        parameters = [["s", self.sprite_type], ["p", partner.name]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def dissapear(self):
        """ Eliminates the object """
        pass

        name = self.sprite_name + "_DISSAPEAR"
        parameters = [["s", self.sprite_type]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def chase(self, partner):
        """ Choose the movement that moves toward the closest sprite of the 
        partner type """
        pass

        name = self.sprite_name + "_CHASE"
        parameters = [["s", self.sprite_type], ["p", partner.name]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        

    # -------------------------------------------------------------------------

    def flee(self, partner):
        """ Choose the movement that moves away the closest sprite of the
        partner type """        
        pass

        name = self.sprite_name + "_FLEE"
        parameters = [["s", self.sprite_type], ["p", partner.name]]        
        conditions = []
        effects = []

        return Action(name, parameters, conditions, effects)        


###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

class ObjectMethods:
    """ Return methods depending of the sprite (not including avatars) """

    def __init__(self, sprite_name, sprite_type):
        self.sprite_name = sprite_name
        self.sprite_type = sprite_type

    # -------------------------------------------------------------------------

    def get_methods(self):
        methods = []

        # Not clear what it does
        # Missile that produces object at a specific ratio
        if self.sprite_type == "Bomber":    
            # methods.append(self.produce(partner))        
            # methods.append(self.move(direction ??))
            pass

        # Follows partner (or avatar ?) object
        if self.sprite_type == "Chaser":    
            # methods.append(self.follow(partner))        
            pass

        # Missile that randomly changes direction
        if self.sprite_type == "ErraticMissile":     
            # methods.append(self.move(direction ??))                   
            # methods.append(self.changeDirection()) - DOESN'T MAKE SENSE TO BE AN method, IT'S RANDOM
            pass

        # Try to make the greatest distance with the partner (or avatar) object
        if self.sprite_type == "Fleeing":       
            # methods.append(self.flee(partner))     
            pass

        # Maybe not needed here
        # Object that dissapear after a moment
        if self.sprite_type == "Flicker":
            # methods.append(self.disappear())
            pass

        # Object that moves constantly in one direction
        if self.sprite_type == "Missile":          
            # methods.append(self.move(direction ??))              
            pass

        # Maybe not needed here
        # Oriented object that dissapear after a moment
        if self.sprite_type == "OrientedFlicker":            
            # methods.append(self.dissapear())
            pass

        # Acts like a Chaser but sometimes it makes a random move
        if self.sprite_type == "RandomAltChaser":  
            # The same methods that Chaser, random moves don't need to be defined
            pass
        
        # Acts like a Bomber but randomly change direction
        if self.sprite_type == "RandomBomber":            
            # The same methods that Bomber, random moves don't need to be defined
            pass

        # Acts like a Missile but randomly change direction
        if self.sprite_type == "RandomMissile":            
            # The same methods that Missile, random moves don't need to be defined
            pass

        # Chooses randomly an method in each iteration
        if self.sprite_type == "RandomNPC":         
            # We can't know wich method will he choose, probably this will be empty  
            # In case we want to add something, we should add each method of the NPC 
            pass

        # Produces objects following a specific ratio
        if self.sprite_type == "SpawnPoint":  
            # methods.append(self.produce(partner))          
            pass

        # Expands in 4 directions if not occupied
        if self.sprite_type == "Spreader":       
            # methods.append(self.expand())     
            pass

        # Missile that if when it collides it change to a random direction
        if self.sprite_type == "Walker":
            # methods.append(self.move(direction ??))
            # If collides stop calculating until we know the new direction
            pass

        # Not clear what it does
        if self.sprite_type == "WalkerJumper":            
            pass

       
        return methods

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def move(self, direction):
        name = self.sprite_name + "_MOVE"
        preconditions = []
        actions = ["(" + self.sprite_name + "_MOVE ?s ?p)"]    
        
        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    def expand(self):
        name = self.sprite_name + "_EXPAND"
        preconditions = []
        actions = ["(" + self.sprite_name + "_EXPAND ?s ?p)"]    
        
        return Method(name, preconditions, actions)
    
    # -------------------------------------------------------------------------

    def produce(self, partner):        
        name = self.sprite_name + "_PRODUCE"
        preconditions = []
        actions = ["(" + self.sprite_name + "_PRODUCE ?s ?p)"]    
        
        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    def dissapear(self):
        name = self.sprite_name + "_DISSAPEAR"
        preconditions = []
        actions = ["(" + self.sprite_name + "_DISSAPEAR ?s ?p)"]    
        
        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    def chase(self, partner):
        name = self.sprite_name + "_CHASE"
        preconditions = []
        actions = ["(" + self.sprite_name + "_CHASE ?s ?p)"]    
        
        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    def flee(self, partner):
        name = self.sprite_name + "_FLEE"
        preconditions = []
        actions = ["(" + self.sprite_name + "_FLEE ?s ?p)"]    
        
        return Method(name, preconditions, actions)
