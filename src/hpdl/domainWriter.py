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
        types - functions - predicates - tasks - actions
    """
    def __init__(self, types, functions, predicates, tasks, actions):
        self.text_domain = self.get_domain_definition()
        self.text_domain += self.get_types(types)
        # self.text_domain += self.get_predicates(predicates)
        self.text_domain += self.get_functions(functions)
        self.text_domain += self.get_tasks(tasks)
        self.text_domain += self.get_actions(actions)
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
        text_content = "\t"

        for t in types:
            type_class = t[0]

            for i in range(1, len(t)):
                text_content += " " + t[i]

            text_content += " - " + type_class + "\n\t\t"

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

        text_content = "\t"

        for f in functions:
            text_content += f + "\n\t\t"

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

        text_content = "\t"

        for p in predicates:
            text_content += p + "\n\t\t"

        return start_text + text_content + end_text

    # -------------------------------------------------------------------------

    def get_tasks(self, tasks):
        """ Returns a string with the task definition

        Arguments:
            tasks       list of Task
        """
        text = "\n\t"

        for t in tasks:
            text_method = ""

            for m in t.methods:                
                text_method += ("\n\t\t(:method " + m.name + "\n\t\t\t\t:precondition ( " 
                               + m.get_preconditions() + ")\n\t\t\t\t:tasks ( " 
                               + m.get_tasks() + " )\n\t\t)\n")

            text_task = ("(:task """ + t.name + "\n\t\t:parameters (" + t.get_parameters()
                        + ")\n" + text_method + "\t)")

            text += text_task + "\n"

        return text

    # -------------------------------------------------------------------------

    def get_actions(self, actions):
        """ Returns a string with the actions definition
    
        Arguments:
            actions     list of Action
        """
        text = "\n"

        for a in actions:
            text_action = ("\t(:action """ + a.name + "\n\t\t:parameters ( "
                        + a.get_parameters()
                        + ")\n\t\t:condition (and\n\t\t\t\t\t\t\t\t\t" 
                        + a.get_conditions()
                        + "\n\t\t\t\t\t\t\t )\n\t\t:effect (and\n\t\t\t\t\t\t\t\t" 
                        + a.get_effects() + "\n\t\t\t\t\t\t)")

            text += text_action + "\n"

        return text