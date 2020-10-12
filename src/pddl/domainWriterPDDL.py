###############################################################################
# domainWriterPDDL.py
# Ignacio Vellido Expósito
# 28/09/2020
#
# Produces a PDDL domain receiving each part separately
###############################################################################


class DomainWriterPDDL:
    """ Produces a string with a PDDL domain 

        Arguments (all list of strings):
            types - functions - predicates - tasks - actions
    """

    def __init__(
        self,
        types: list,
        constants: list,
        functions: list,    # Ignored
        predicates: list,
        tasks: list,        # Ignored
        actions: list,
    ):
        self.text_domain = self.get_domain_definition()
        self.text_domain += self.get_types(types)
        self.text_domain += self.get_constants(constants)
        self.text_domain += self.get_predicates(predicates)
        # self.text_domain += self.get_functions(functions)
        # self.text_domain += self.get_tasks(tasks)
        self.text_domain += self.get_actions(actions)
        self.text_domain += self.get_end_domain()

    # -------------------------------------------------------------------------

    def get_domain(self) -> str:
        return self.text_domain

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    # Returns a string containing the domain definition
    def get_domain_definition(self):
        text = """
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; PDDL domain for a VGDL game
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain VGDLGame)  
\t(:requirements
\t\t:adl
\t\t:negative-preconditions
\t)
"""
        return text

    # -------------------------------------------------------------------------

    # Returns a string with closing the final brackets in the domain
    def get_end_domain(self):
        text = """
)
"""
        return text

    # -------------------------------------------------------------------------

    def get_types(self, types):
        """ Returns a string with the types definition
    
        types: 2D array, in each line, first value represents the type, the 
        rest are the name of the objects
        """
        start_text = """
\t; Types ---------------------------------------------------------------------

\t(:types"""

        end_text = """
\t)
"""
        text_content = ""

        for t in types:
            text_content += "\n\t\t"

            type_class = t[0]

            if t[1] == "":
                text_content += type_class
            else:
                for i in range(1, len(t)):
                    text_content += t[i] + " "

                text_content += "- " + type_class

        return start_text + text_content + end_text

    # -------------------------------------------------------------------------

    def get_constants(self, constants):
        """ Returns a string with the constants definition
    
        constants: 2D array, in each line, first value represents the class, the 
        rest are the name of the constants
        """
        start_text = """
\t; Constants -----------------------------------------------------------------

\t(:constants"""

        end_text = """
\t)
"""
        text_content = ""

        for c in constants:
            text_content += "\n\t\t"

            type_class = c[0]

            if c[1] == "":
                text_content += type_class
            else:
                for i in range(1, len(c)):
                    text_content += c[i] + " "

                text_content += "- " + type_class

        return start_text + text_content + end_text

    # -------------------------------------------------------------------------
    # NOT CONSIDERING FUNCTIONS IN PDDL
    # Being limited by multiple planners make it not worthy
    # -------------------------------------------------------------------------

#     def get_functions(self, functions):
#         """ Returns a string with the functions definition
    
#         functions: list of functions, in brackets
#         """
#         start_text = """
# \t; Functions -----------------------------------------------------------------

# \t(:functions"""

#         end_text = """
# \t)
# """
#         text_content = ""

#         for f in functions:
#             text_content += "\n\t\t" + f

#         return start_text + text_content + end_text

    # -------------------------------------------------------------------------

    def get_predicates(self, predicates):
        """ Returns a string with the predicates definition
    
        predicates: list of predicates, in brackets
        """
        start_text = """
\t; Predicates ----------------------------------------------------------------
\n\t(:predicates"""
        end_text = """
\t)
  """

        text_content = ""

        for p in predicates:
            text_content += "\n\t\t" + p

        return start_text + text_content + end_text

    # -------------------------------------------------------------------------

    def get_actions(self, actions):
        """ Returns a string with the actions definition
    
        Arguments:
            actions     list of Action
        """
        start_text = """
\t; Actions -------------------------------------------------------------------
  """

        text = "\n"

        for a in actions:
            preconditions = a.get_preconditions()
            effects = a.get_effects()

            # If it don't begins with a forall
            if len(a.effects) > 0 and not "forall" in a.effects[0]:
                text_effects = "and " + effects
            else:
                text_effects = effects

            text += (
                "\t(:action "
                ""
                + a.name
                + "\n\t\t:parameters ("
                + a.get_parameters()
                + ")\n\t\t:precondition ("
                + ("" if not preconditions else ("and " + preconditions))
                + "\n\t\t\t\t\t)\n\t\t:effect ("
                + ("" if not effects else text_effects)
                + "\n\t\t\t\t)\n\t)\n\n"
            )

        return start_text + text
