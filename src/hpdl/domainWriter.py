###############################################################################
# domainWriter.py
# Ignacio Vellido Expósito
# 23/08/2019
# 
# Produces a HPDL domain(
###############################################################################

class DomainWriter:
    """ Produces a string with a HPDL domain 

    Arguments:
        types - functions - predicates - actions
    """
    def __init__(self, types, functions, predicates, actions):
        self.text_domain = self.get_domain_definition()
        self.text_domain += self.get_types(types)
        # self.text_domain += self.get_predicates(predicates)
        self.text_domain += self.get_functions(functions)
        # self.text_domain += self.get_actions(actions)
        self.text_domain += self.get_end_domain()

    def get_domain(self):
        return self.text_domain

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    # Returns a string containing the domain definition
    def get_domain_definition(self):
        text = """
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; HPDL domain for a VGDL game
;;; Made with antlr-vgdl
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain VGDLGame)  
  (:requirements
    :typing
    :fluents
    :derived-predicates
    :negative-preconditions
    :universal-preconditions
    :disjuntive-preconditions
    :conditional-effects
    :htn-expansion

    ; For time management
    :durative-actions
    :metatags
  )
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
  (:types    
  """
        end_text = """
  )
  """
        text_content = "  "

        for t in types:
            type_class = t[0]

            for i in range(1, len(t)):
                text_content += " " + t[i]

            text_content += " - " + type_class + "\n    "

        return start_text + text_content + end_text

    # -------------------------------------------------------------------------
    
    def get_functions(self, functions):
        """ Returns a string with the functions definition
    
        functions: list of functions, in brackets
        """
        start_text = """
  (:functions    
  """
        end_text = """
  )
  """

        text_content = "  "

        for f in functions:
            text_content += f + "\n    "

        return start_text + text_content + end_text


    # -------------------------------------------------------------------------

    def get_predicates(self, predicates):
        """ Returns a string with the predicates definition
    
        predicates: list of predicates, in brackets
        """
        start_text = """
  (:predicates    
  """
        end_text = """
  )
  """

        text_content = "  "

        for p in predicates:
            text_content += p + "\n    "

        return start_text + text_content + end_text


    # -------------------------------------------------------------------------

    def get_actions(actions):
        """ Returns a string with the actions definition
    
        actions: list of actions
        """
        text = ""

        for a in actions:
            text += a

        return text
