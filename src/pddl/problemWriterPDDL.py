###############################################################################
# problemWriterPDDL.py
# Ignacio Vellido Expósito
# 28/09/2020
#
# Produces a PDDL problem receiving each part separately
###############################################################################


class ProblemWriterPDDL:
    """ Produces a string with a PDDL domain 

        Arguments:
            objects     List of strings
            init        List of strings
            goals       List of strings
    """

    def __init__(self, objects: list, init: list, goals: list):
        self.text_problem = self.get_problem_definition()
        self.text_problem += self.get_objects(objects)
        self.text_problem += self.get_init(init)
        self.text_problem += self.get_goals(goals)
        self.text_problem += self.get_end_problem()

    def get_problem(self) -> str:
        return self.text_problem

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def get_problem_definition(self):
        """ Returns a string containing the domain definition """
        text = """
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; PDDL problem for a VGDL game
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (problem VGDLProblem) (:domain VGDLGame)
"""
        return text

    # -------------------------------------------------------------------------

    def get_end_problem(self):
        """ Returns a string with closing the final brackets in the domain """
        text = """
)
"""
        return text

    # -------------------------------------------------------------------------

    def get_objects(self, objects):
        """ Returns a string with the types definition
    
        objects: 2D array, in each line, first value represents the type, the 
        rest are the name of the objects
        """
        start_text = """
\t; Objects ---------------------------------------------------------------------

\t(:objects"""

        end_text = """
\t)
"""
        text_content = ""

        for o in objects:
            text_content += "\n\t\t\t" + o

        return start_text + text_content + end_text

    # -------------------------------------------------------------------------

    def get_init(self, init):
        """ Returns a string with the init definition
    
        init: 2D array. In each line the predicate to be included, with brackets
        """
        start_text = """
\t; Init -----------------------------------------------------------------

\t(:init"""

        end_text = """
\t)
"""
        text_content = ""

        for i in init:
            text_content += "\n\t\t\t" + i

        return start_text + text_content + end_text

    # -------------------------------------------------------------------------

    def get_goals(self, goals):
        """ Returns a string with the task-goal definition
    
        goal: list of goals, in brackets
        """
        start_text = """
\t; Goals -----------------------------------------------------------------

\t(:tasks-goal
\t\t:tasks("""

        end_text = """
\t\t)
\t)
"""
        text_content = ""

        for g in goals:
            text_content += "\n\t\t\t" + g

        return start_text + text_content + end_text

    # -------------------------------------------------------------------------
