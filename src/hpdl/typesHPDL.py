###############################################################################
# typesHPDL.py
# Ignacio Vellido Expósito
# 26/08/2019
# 
# Multiple classes defining parts of a HPDL domain
###############################################################################

class Task:
    """ Defines the structure of a task in HPDL

    Atributes:
        name            String
        parameters      List of pairs <alias, type>
        methods         List
    """
    def __init__(self, name, parameters, methods):
        self.name = name
        self.parameters = parameters
        self.methods = methods

    def get_parameters(self):
        """ Returns list of parameters without external brackets """
        text = " "

        for p in self.parameters:
            text += "?" + p[0] + " - " + p[1] + " "

        return text


# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------

class Method:
    """ Defines the structure of a method in HPDL

    Atributes:
        name             String
        preconditions    List
        task_predicates  List of tasks. Their calling way, not the objects
    """
    def __init__(self, name, preconditions, task_predicates):
        self.name = name
        self.preconditions = preconditions
        self.task_predicates = task_predicates
    
    def get_preconditions(self):
        """ Returns list of preconditions without external brackets """
        text = ""

        # If list not empty
        if self.preconditions:
            for c in self.preconditions:
                text += "\n\t\t\t\t\t\t\t\t\t" + c

        return text

    def get_tasks(self):
        """ Returns list of tasks without (global) external brackets """
        text = ""

        if self.task_predicates:
            for t in self.task_predicates:
                text += "\n\t\t\t\t\t\t\t" + t

        return text

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------

class Action:
    """ Defines the structure of a method in HPDL

    Atributes:
        name            String
        parameters      List of pairs <alias, type>
        preconditions   List of predicates, with brackets
        effects         List of effects, with brackets
    """
    def __init__(self, name, parameters, preconditions, effects):
        self.name = name
        self.parameters = parameters
        self.preconditions = preconditions
        self.effects = effects

    def get_parameters(self):
        """ Returns list of parameters without external brackets """
        text = ""

        for p in self.parameters:
            text += "?" + p[0] + " - " + p[1] + " "

        return text

    def get_preconditions(self):
        """ Returns list of conditions without external brackets """
        text = ""

        for c in self.preconditions:
            text += "\n\t\t\t\t\t\t" + c

        return text

    def get_effects(self):
        """ Returns list of effects without external brackets """
        text = ""

        for e in self.effects:
            text += "\n\t\t\t\t\t" + e

        return text