###############################################################################
# typesPDDL.py
# Ignacio Vellido Expósito
# 28/09/2020
#
# Multiple classes defining parts of a PDDL domain
###############################################################################


class Task:
    """ Defines the structure of a task in PDDL

        Atributes:
            name            String
            parameters      List of pairs <alias, type>
            methods         List
    """

    def __init__(self, name: str, parameters: list, methods: list):
        self.name = name
        self.parameters = parameters
        self.methods = methods

    # --------------------------------------------------------------------------

    def get_parameters(self) -> str:
        """ Returns string of parameters without external brackets """
        text = " "

        for p in self.parameters:
            text += "?" + p[0] + " - " + p[1] + " "

        return text


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


class Method:
    """ Defines the structure of a method in PDDL

        Atributes:
            name             String
            preconditions    List
            task_predicates  List of tasks. Their calling way, not the objects
    """

    def __init__(self, name: str, preconditions: list, task_predicates: list):
        self.name = name
        self.preconditions = preconditions
        self.task_predicates = task_predicates

    # --------------------------------------------------------------------------

    def get_preconditions(self) -> str:
        """ Returns string of preconditions without external brackets """
        text = ""

        # If list not empty
        if self.preconditions:
            for c in self.preconditions:
                text += "\n\t\t\t\t\t\t\t\t\t" + c

        return text

    # --------------------------------------------------------------------------

    def get_tasks(self) -> str:
        """ Returns string of tasks without (global) external brackets """
        text = ""

        if self.task_predicates:
            for t in self.task_predicates:
                text += "\n\t\t\t\t\t\t\t" + t

        return text


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


class Action:
    """ Defines the structure of a method in PDDL

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

    # --------------------------------------------------------------------------

    def get_parameters(self) -> str:
        """ Returns string of parameters without external brackets """
        text = ""

        for p in self.parameters:
            text += "?" + p[0] + " - " + p[1] + " "

        return text

    # --------------------------------------------------------------------------

    def get_preconditions(self):
        """ Returns string of conditions without external brackets """
        text = ""

        for c in self.preconditions:
            text += "\n\t\t\t\t\t\t" + c

        return text

    # --------------------------------------------------------------------------

    def get_effects(self) -> str:
        """ Returns string of effects without external brackets """
        text = ""

        for e in self.effects:
            text += "\n\t\t\t\t\t" + e

        return text
