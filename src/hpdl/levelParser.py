###############################################################################
# levelParser.py
# Ignacio Vellido Expósito
# 11/10/2019
# 
# Parse a VGDL level definition into a HPDL problem
###############################################################################

import string
from itertools import permutations

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

class LevelObject:
    def __init__(self, name, row, col, stype):
        self.name = name
        self.row  = row
        self.col  = col
        self.stype = stype

    def toStr(self):
        return self.name + "-" + str(self.row) + "," + str(self.col) + \
                "-" + self.stype

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def read_level(path):  
    try:
        with open(path, "r") as file:
            return file.read()            
    except Exception as e:
        print("Cannot open file " + path)
        print(str(e))


# -----------------------------------------------------------------------------

def parse_level(level, short_types, long_types):
    """ Returns a list of LevelObjects with the objects defined 
    
    short_types and long_types must have same length, defines the stype of the
    object and the char used in the level to represent it
    """
    
    lines = level.splitlines()

    row = col = 0
    objects = []

    # To keep track of each object defined and assign differents names
    # A list of the size of types with zeros
    name_counters = [0] * len(short_types)

    # To calculate the maximum number of objects in the game
    max_size = 0

    # --------------------------------------------------------------------------
    # Some characters can create problems on the domain, it is necessary
    # to change them            
    valid_char = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    valid_used_char = valid_char.copy()
    changed_char = []
    number = 1

    # Removing the used chars        
    for m in short_types:
        try:
            valid_char.remove(m)
        except Exception as e:
            pass

    for m in short_types:
        # Because there can be mora tan 52 objects on the game, we add a 
        # counter at the end of the char if needed
        if not valid_char:
            valid_char = list(string.ascii_lowercase) + list(string.ascii_uppercase)
            number += 1

        if m not in valid_used_char:
            old_char = m
            m = valid_char.pop()  

            # Replacing
            changed_char.append([old_char, m])
            short_types = [m if x == old_char else x for x in short_types]

    # ------------------------------------------------

    # Creating the LevelObjects
    for line in lines:
        for char in line:
            # Not considering spaces
            if char is not ' ' or char is not '\t':                
                # Checking for wrong characters
                if char not in valid_used_char:
                    for change in changed_char:
                        if char == change[0]:
                            char = change[1]
                            changed = True

                    # If char not found
                    if not changed:
                        raise ValueError (
                            "Wrong level definition: " + char + " not defined"
                        )

                indx = short_types.index(char)
                obj = LevelObject(char + str(name_counters[indx]), row, col,
                                    long_types[indx])                
                objects.append(obj)

                name_counters[indx] += 1

                max_size += 1
                col += 1
        
        col = 0
        row += 1    

    # Completing the definition of objects
    for (lt, st, c) in zip(long_types, short_types, name_counters):
        if "avatar" not in lt.lower():
            while c < max_size:
                obj = LevelObject(st + str(c), -1, -1, lt)
                objects.append(obj)

                c += 1

    return objects, max_size, short_types, name_counters

# -----------------------------------------------------------------------------

def get_problem(objects, counters, short_types, long_types, 
                    max_size, hierarchy, stypes):
    problem = ""

    problem += """
(define (problem VGDLProblem) (:domain VGDLGame)
    (:objects"""
    # Defining objects
    for obj in objects:
        # First writing each one separately, but a better aproach would be to get 
        # all objects of the same type written in the same line        
        problem += "\n\t\t" + obj.name + " - " + obj.stype

    # Init part
    problem += """
    )

    (:init
        (= (turn) 0)"""
    for obj in objects:
        # --------------------------------------------
        # Writing predicates, if any
        # Que reciba por parámetro los predicados ?s
        # Si es avatar, misil, recurso
        predicates = ""

        # Only for boulderdash
        if "avatar" in obj.stype.lower():      
            avatar = obj.name
            predicates += "\n\t\t(can-move-up " + avatar + ")"
            predicates += "\n\t\t(can-move-down " + avatar + ")"
            predicates += "\n\t\t(can-move-left " + avatar + ")"
            predicates += "\n\t\t(can-move-right " + avatar + ")"
            predicates += "\n\t\t(can-use " + avatar + ")"
            predicates += "\n\t\t(can-change-orientation " + avatar + ")"
            predicates += "\n\t\t(orientation-up " + avatar + ")"
            predicates += "\n\t\t(= (resource_diamond " + avatar + ") 0)"

        if "boulder" in obj.stype.lower():      
            predicates += "\n\t\t(orientation-down " + obj.name + ")"

        #---------------------------------------------
        # Writing the coordinates of the objects
        coordinates = "\n\t\t(= (coordinate_x " + obj.name + ") " + str(obj.row) + ")"
        coordinates += "\n\t\t(= (coordinate_y " + obj.name + ") " + str(obj.col) + ")"
        coordinates += "\n\t\t(= (last_coordinate_x " + obj.name + ") -1)"
        coordinates += "\n\t\t(= (last_coordinate_y " + obj.name + ") -1)"

        #---------------------------------------------
        # Writing the evaluate-interaction predicates
        # Fastest way tested, even comparing with itertools (20 times worse)
        evaluate = ""
        for obj2 in objects:
            if obj is not obj2:
                evaluate += "\n\t\t(evaluate-interaction " + obj.name + " " + obj2.name + ")"

        problem += predicates + coordinates + evaluate + "\n"


    # Writing the counters    
    all_counters = dict.fromkeys(stypes, 0)
    for c, name in zip(counters, long_types):
        all_counters[name] = c

        for parent in hierarchy[name]:
            all_counters[parent] += c        

    for obj in all_counters:
        if obj:     # Hay un objeto None que no debería estar
            problem += "\n\t\t" + "(= (counter_" + obj + ") " + str(all_counters[obj]) + ")"
        

    # Writing goal
    problem += """
    )

    (:tasks-goal
        :tasks(
            (Turn)
        )
    )
)
"""
    return problem