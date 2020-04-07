###############################################################################
# problemGeneratorHPDL.py
# Ignacio Vellido Expósito
# 11/10/2019
#
# Parse a VGDL level definition into a HPDL problem
###############################################################################

import string

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


class LevelObject:
    """ Structure containing information of a sprite defined in a level """

    def __init__(self, name: str, row: int, col: int, stype: str):
        self.name = name
        self.row = row
        self.col = col
        self.stype = stype

    def toStr(self) -> str:
        return self.name + "-" + str(self.row) + "," + str(self.col) + "-" + self.stype


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


class ProblemGeneratorHPDL:
    """ Generates the different parts of a HPDL problem """

    def __init__(
        self,
        level,
        short_types,
        long_types,
        transformTo,
        hierarchy,
        stypes,
        sprites,
        avatarHPDL,
        spritesHPDL,
    ):
        self.objects = []
        self.init = []
        self.goals = []

        self.level = level
        self.short_types = short_types
        self.long_types = long_types
        self.transformTo = transformTo
        self.hierarchy = hierarchy
        self.stypes = stypes
        self.sprites = sprites
        self.avatarHPDL = avatarHPDL
        self.spritesHPDL = spritesHPDL

        self.max_size = 0  # To calculate the maximum number of objects in the game

        # To keep track of each object defined and assign differents names
        # A list of the size of types with zeros
        self.name_counters = [0] * len(self.short_types)
        self.levelObjects = []

        self.parse_level()

        # Adding the partner of the avatar (if exists) as a levelObject
        if avatarHPDL.partner:
            self.levelObjects.append(LevelObject("partner", -1, -1, avatarHPDL.partner.name))

        self.assign_objects()
        self.assign_init()
        self.assign_goals()

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    def assign_goals(self):
        self.goals = ["(Turn)"]

    # --------------------------------------------------------------------------

    def assign_objects(self):
        for obj in self.levelObjects:
            # First writing each one separately, but a better aproach would be to get
            # all objects of the same type written in the same line
            self.objects.append(obj.name + " - " + obj.stype)

    # --------------------------------------------------------------------------

    def assign_init(self):
        self.init.append("(= (turn) 0)")

        # Init part
        for obj in self.levelObjects:
            # --------------------------------------------
            # Writing object-specific predicates, if any

            # Avatar-specific predicates
            if "avatar" in obj.stype.lower():
                avatar_name = obj.name
                for pred in self.avatarHPDL.level_predicates:
                    self.init.append(pred.replace("?a", avatar_name))

            else:  # The rest of the objects
                sprite_name = obj.name

                for spriteHPDL in self.spritesHPDL:
                    if spriteHPDL.sprite.stype in self.hierarchy[obj.stype]:
                        for pred in spriteHPDL.level_predicates:
                            self.init.append(pred.replace("?o", sprite_name))

            # ---------------------------------------------
            # Writing the coordinates of the objects
            self.init.append("(= (coordinate_x " + obj.name + ") " + str(obj.col) + ")")
            self.init.append("(= (coordinate_y " + obj.name + ") " + str(obj.row) + ")")
            self.init.append(
                "(= (last_coordinate_x " + obj.name + ") " + str(obj.col) + ")"
            )
            self.init.append(
                "(= (last_coordinate_y " + obj.name + ") " + str(obj.row) + ")"
            )

            # ---------------------------------------------
            # Writing the evaluate-interaction predicates
            # Fastest way tested, even comparing with itertools (20 times worse)
            for obj2 in self.levelObjects:
                if obj is not obj2:
                    self.init.append(
                        "(evaluate-interaction " + obj.name + " " + obj2.name + ")"
                    )

            self.init.append("\n")

        # Writing the counters
        all_counters = dict.fromkeys(self.stypes, 0)
        for c, name in zip(self.name_counters, self.long_types):
            all_counters[name] = c

            for parent in self.hierarchy[name]:
                all_counters[parent] += c

        for obj in all_counters:
            if obj:  # Hay un objeto None que no debería estar
                self.init.append(
                    "(= (counter_" + obj + ") " + str(all_counters[obj]) + ")"
                )

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    def parse_level(self):
        """ Returns a list of LevelObjects with the objects defined 
        
        short_types and long_types must have same length, defines the stype of the
        object and the char used in the level to represent it
        """

        lines = self.level.splitlines()

        row = col = 0

        # --------------------------------------------------------------------------
        # Some characters can create problems on the domain, it is necessary
        # to change them
        valid_char = list(string.ascii_lowercase) + list(string.ascii_uppercase)
        valid_used_char = valid_char.copy()
        changed_char = []
        number = 1

        # Removing the used chars
        for m in self.short_types:
            try:
                valid_char.remove(m)
            except Exception as e:
                pass

        for m in self.short_types:
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
                self.short_types = [m if x == old_char else x for x in self.short_types]

        # ----------------------------------------------------------------------

        # Creating the LevelObjects
        for line in lines:
            for char in line:
                # Not considering spaces
                if char is not " " or char is not "\t":
                    # Checking for wrong characters
                    if char not in valid_used_char:
                        for change in changed_char:
                            if char == change[0]:
                                char = change[1]
                                changed = True

                    # Wrong level definition
                    if char not in self.short_types:
                        print("[ERROR] Wrong character in level definition ")
                        print("Produced by: ", char)
                        exit()

                    indx = self.short_types.index(char)
                    obj = LevelObject(
                        char + str(self.name_counters[indx]),
                        row,
                        col,
                        self.long_types[indx],
                    )
                    self.levelObjects.append(obj)

                    self.name_counters[indx] += 1

                    self.max_size += 1
                    col += 1

            col = 0
            row += 1

        # ----------------------------------------------------------------------
        # Completing the definition of levelObjects

        # Finding his associated short_type (There should be a better way)
        for tt in self.transformTo:
            for (lt, st, c) in zip(
                self.long_types, self.short_types, self.name_counters
            ):
                if tt == lt:
                    while c < self.max_size:
                        obj = LevelObject(st + str(c), -1, -1, lt)
                        self.levelObjects.append(obj)

                        c += 1

        return self.levelObjects, self.max_size, self.short_types, self.name_counters

    # --------------------------------------------------------------------------
