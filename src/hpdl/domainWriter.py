###############################################################################
# domainWriter.py
# Ignacio Vellido Expósito
# 23/08/2019
# 
# Produces a HPDL domain
###############################################################################

class DomainWriter:
    """ Produces a string with a HPDL domain 

    Arguments:
        types - functions - predicates - tasks - actions
    """
    def __init__(self, types, functions, predicates, tasks, actions):
        self.text_domain = self.get_domain_definition()
        self.text_domain += self.get_types(types)
        self.text_domain += self.get_predicates(predicates)
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
\t(:requirements
\t\t:typing
\t\t:fluents
\t\t:derived-predicates
\t\t:negative-preconditions
\t\t:universal-preconditions
\t\t:disjuntive-preconditions
\t\t:conditional-effects
\t\t:htn-expansion

\t\t; For time management
\t\t:durative-actions
\t\t:metatags
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
\t; Types -----------------------------------------------------------------....

\t(:types    
  """
        end_text = """
\t)
  """
        text_content = "\t\t"

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
\t; Functions -----------------------------------------------------------------

\t(:functions    
  """
        end_text = """
\t)
  """

        text_content = ""

        for f in functions:
            text_content += "\n\t\t" + f

        return start_text + text_content + end_text


    # -------------------------------------------------------------------------

    def get_predicates(self, predicates):
        """ Returns a string with the predicates definition
    
        predicates: list of predicates, in brackets
        """
        start_text = """
\t; Predicates ----------------------------------------------------------------
\t(:predicates    
  """
        end_text = """
\t)
  """

        text_content = ""

        for p in predicates:
            text_content += "\n\t\t" + p

        return start_text + text_content + end_text

    # -------------------------------------------------------------------------

    def get_tasks(self, tasks):
        """ Returns a string with the task definition

        Arguments:
            tasks       list of Task
        """
        start_text = """
\t; Tasks ---------------------------------------------------------------------
  """
        text = "\n\t"

        for t in tasks:
            text_method = ""

            for m in t.methods:                
                text_method += ("\n\t\t(:method " + m.name + "\n\t\t\t\t:precondition ( " 
                               + m.get_preconditions() + ")\n\t\t\t\t:tasks ( " 
                               + m.get_tasks() + " )\n\t\t)\n")

            text_task = ("(:task """ + t.name + "\n\t\t:parameters (" + t.get_parameters()
                        + ")\n" + text_method + "\t)\n")

            text += text_task + "\n"

        return start_text + text

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
            text  += ("\t(:action """ + a.name + "\n\t\t:parameters ( "
                     + a.get_parameters()
                     + ")\n\t\t:condition (and\n\t\t\t\t\t\t" 
                     + a.get_conditions()
                     + "\n\t\t\t\t\t)\n\t\t:effect (and\n\t\t\t\t\t" 
                     + a.get_effects() + "\n\t\t\t\t)\n\t)\n\n")

        return start_text + text