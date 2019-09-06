###############################################################################
# methodsGenerators.py
# Ignacio Vellido Expósito
# 05/09/2019
# 
# Each class produces methods for a HPDL domain
###############################################################################

from hpdl.hpdlTypes import Method

###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

# RECIEVE partner IN initializer ?

class AvatarMethodsGenerator:
    """ Returns different methods depending of the avatar """
    def __init__(self, avatar_name, avatar_type):
        self.avatar_name = avatar_name
        self.avatar_type = avatar_type

    def get_methods(self, partner=None):
        """ Return a list of methods depending of the avatar 
        
        partner:    If ACTION_USE is available for the avatar, 'partner' is the 
                    sprite that is produced
        """
        methods = []
        methods.append(self.nil()) # Don't do anything

        # Can't move but can use object
        if self.avatar_type == "AimedAvatar":
            # methods.append(self.turn_up())
            # methods.append(self.turn_down())
            # methods.append(self.turn_left())
            # methods.append(self.turn_right())
            # methods.append(self.use(partner))
            pass

        # This avatar should have ammo
        # Always same orientation, can move horizontally and use object
        if self.avatar_type == "FlakAvatar":
            methods.append(self.move_left())
            methods.append(self.move_right())
            # methods.append(self.use(partner))

        # Always same orientation, can only move left or right
        if self.avatar_type == "HorizontalAvatar":
            # methods.append(self.move_left())
            # methods.append(self.move_right())
            pass            

        # Always same orientation, can move in any direction
        if self.avatar_type == "MovingAvatar":
            # methods.append(self.move_up())
            # methods.append(self.move_down())
            # methods.append(self.move_left())
            # methods.append(self.move_right())
            pass       

        # ONLY GVGAI
        if self.avatar_type == "OngoingShootAvatar":
            pass

        # ONLY GVGAI
        if self.avatar_type == "OngoingTurningAvatar":
            pass

        # Can move and aim in any direction
        if self.avatar_type == "OrientedAvatar":
            # methods.append(self.move_up())
            # methods.append(self.move_down())
            # methods.append(self.move_left())
            # methods.append(self.move_right())
            # methods.append(self.turn_up())
            # methods.append(self.turn_down())
            # methods.append(self.turn_left())
            # methods.append(self.turn_right())
            pass
        
        # Can move and aim in any direction, can use object
        if self.avatar_type == "ShootAvatar":
            methods.append(self.move_up())
            methods.append(self.move_down())
            methods.append(self.move_left())
            methods.append(self.move_right())
            methods.append(self.turn_up())
            methods.append(self.turn_down())
            methods.append(self.turn_left())
            methods.append(self.turn_right())
            # methods.append(self.use(partner))

        # Always same orientation, can only move up or down
        if self.avatar_type == "VerticalAvatar":
            # methods.append(self.move_up())
            # methods.append(self.move_down())
            pass
        
        return methods


        # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def move_up(self):
        name = "move_up"
        preconditions = []
        actions = ["(AVATAR_MOVE_UP ?a ?o)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    def move_down(self):
        name = "move_down"
        preconditions = []
        actions = ["(AVATAR_MOVE_DOWN ?a ?o)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    def move_left(self):
        name = "move_left"
        preconditions = []
        actions = ["(AVATAR_MOVE_LEFT ?a ?o)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    def move_right(self):
        name = "move_right"
        preconditions = []
        actions = ["(AVATAR_MOVE_RIGHT ?a ?o)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    # This method should only be called if the avatar can turn
    def turn_up(self):
        name = "turn_up"
        preconditions = []
        actions = ["(AVATAR_TURN_UP ?a ?o)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    def turn_down(self):
        name = "turn_down"
        preconditions = []
        actions = ["(AVATAR_TURN_DOWN ?a ?o)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    def turn_left(self):
        name = "turn_left"
        preconditions = []
        actions = ["(AVATAR_TURN_LEFT ?a ?o)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    def turn_right(self):
        name = "turn_right"
        preconditions = []
        actions = ["(AVATAR_TURN_RIGHT ?a ?o)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    # Probably will not work
    # can-use is a predicate that should not be active in case there is no ammo
    def use(self, partner):
        """ UNFINISHED """
        name = "use"
        preconditions = []
        actions = ["(AVATAR_USE ?a ?partner)"]    

        return Method(name, preconditions, actions)

    # -------------------------------------------------------------------------

    # Probably will not work
    def nil(self):
        name = "nil"
        preconditions = []
        actions = ["(AVATAR_NIL ?a)"]    

        return Method(name, preconditions, actions)


###############################################################################
# -----------------------------------------------------------------------------
###############################################################################

def SpriteMethodsGenerator():
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
