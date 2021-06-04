###############################################################################
# configurationGenerator.py
# Ignacio Vellido Expósito
# 30/10/2020
#
# Generates the configuration YAML file
###############################################################################

import re

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Basic structure of the configuration file
config = dict(
    domainFile = "domains/simplified-version/domain.pddl",
    problemFile = "problem.pddl",
    domainName = "VGDLGame",
    gameElementsCorrespondence = {},
    variablesTypes = {},    
    avatarVariable = "",
    orientation = {},
    orientationCorrespondence = dict(
        UP = "(oriented-up ?object)",
        DOWN = "(oriented-down ?object)",
        LEFT = "(oriented-left ?object)",
        RIGHT = "(oriented-right ?object)"
    ),
    # connections = dict(
    #     UP = "(connected-up ?c ?u)",
    #     DOWN = "(connected-down ?c ?d)",
    #     LEFT = "(connected-left ?c ?l)",
    #     RIGHT = "(connected-right ?c ?r)",
    # ),
    fluentsPredicates = dict(
        next = "(next ?n0 ?n1)",
        previous = "(previous ?n1 ?n0)"
    ),
    actionsCorrespondence = {},
    additionalPredicates = [
        "(turn-avatar)",
        # ... More added according to the predicates
    ],
    addDeadObjects = {},
    goals = []
)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Listener should not be needed
def get_config(domainGenerator, listener, terminations):
    """ Return configuration YAML 
        - domainGenerator: Contains info about predicates/types ...
        - listener: Contains info about hierarchy/names ...
    """
    predicates = domainGenerator.predicates
    avatar_name = listener.avatar.name
    avatar_predicates = domainGenerator.avatarPDDL.predicates
    spritesPDDL = domainGenerator.spritesPDDL
    actions = domainGenerator.actions

    partner = domainGenerator.partner
    transformTo = listener.transformTo

    # Objects with predicate is-...
    isSomething = ["wall"]
    isSomething.extend([a[0] for a in domainGenerator.killIfHasLess])
    isSomething.extend(domainGenerator.stepbacks)
    
    config_add_gameElementsCorrespondence_variablesTypes(spritesPDDL, 
                                                        avatar_predicates, 
                                                        avatar_name,
                                                        isSomething)
    config_add_avatarVariable(avatar_name)
    config_add_orientation(spritesPDDL, actions, avatar_name)
    config_add_actionsCorrespondence(actions)
    config_add_additionalPredicates()
    config_add_addDeadObjects(partner, transformTo)
    config_add_goals(terminations)
  
    return config

# ------------------------------------------------------------------------------
# Functions producing the multiple sections of the config file
# ------------------------------------------------------------------------------

# Also adds some turn-order related predicates in additionalPredicates
def config_add_gameElementsCorrespondence_variablesTypes(spritesPDDL, avatar_predicates, avatar_name, isSomething):
    config["gameElementsCorrespondence"][avatar_name] = []

    # Avatar predicates
    for predicate in avatar_predicates:
        match = re.search("([\w-])+ ?", predicate) # Only has one occurrence
        config["gameElementsCorrespondence"][avatar_name].append(
            "(%s?%s)" % (match.group(), avatar_name)
        )

    # Get parents
    parents = [sprite.sprite.father for sprite in spritesPDDL]
    parents = list(set([x for x in parents if x is not None]))    

    # Add sprites specific predicates
    for sprite in spritesPDDL:
        name = sprite.sprite.name
        parent = sprite.sprite.father

        # Create empty list
        config["gameElementsCorrespondence"][name] = []


        # Add objects with parents (that have been "simplified") and don't have
        # any particular predicate
        if parent in parents and name != "avatar" and not sprite.predicates:
            config["variablesTypes"]["?%s" % parent] = parent
            config["gameElementsCorrespondence"][name].append(
                "(at ?x ?y ?%s)" % parent,
            )
        elif name not in isSomething and name not in parents:
            # Add variableType
            variableType = "?%s" % name
            config["variablesTypes"][variableType] = name


            config["gameElementsCorrespondence"][name].append(
                "(at ?x ?y ?%s)" % name,
            )

            for pred in sprite.predicates:
                # Check if resource predicate
                if "got-resource" in pred:
                    match = re.search("([\w-])+ ?", pred) # Only has one occurrence
                    config["additionalPredicates"].append(
                        "(%s%s)" % (match.group(), "n0")
                    )
                # Check if the predicate has parameters
                elif "?" in pred: # Add it to specific predicates
                    match = re.search("([\w-])+ ?", pred) # Only has one occurrence
                    config["gameElementsCorrespondence"][name].append(
                        "(%s?%s)" % (match.group(), name)
                    )
                elif not "turn" in pred:   # If no parameters include it directly to additional
                    config["additionalPredicates"].append(pred)


    # Objects with is-... predicate
    for sprite in isSomething:
        config["gameElementsCorrespondence"][sprite].append(
            "(is-%s ?x ?y)" % sprite,
        )

    # Remove empty lists
    for name in parents:        
        if not config["gameElementsCorrespondence"][name]:
            config["gameElementsCorrespondence"].pop(name, None)

    # Remove duplicates
    for name in config["gameElementsCorrespondence"].keys():
        config["gameElementsCorrespondence"][name] = list(set(config["gameElementsCorrespondence"][name]))

    # Add nums to variablesTypes
    config["variablesTypes"]["?x"] = "num"
    config["variablesTypes"]["?y"] = "num"

# ------------------------------------------------------------------------------

def config_add_avatarVariable(avatar_name):
    # Add avatar variable
    config["avatarVariable"] = "?%s" % avatar_name

# ------------------------------------------------------------------------------

def config_add_orientation(spritesPDDL, actions, avatar_name):
    # Adds objects orientation
    for sp in spritesPDDL:
        sprite = sp.sprite        
        orientation = [x for x in sprite.parameters if "orientation" in x]

        if len(orientation) > 0:
            orientation = orientation[0]
            orientation = orientation.split("=")[1]
            config["orientation"][sprite.name] = orientation

    # Check if avatar needs orientation
    config["orientation"][avatar_name] = "FIND" if any("ACTION_TURN" in act.name for act in actions) else "NONE"

# ------------------------------------------------------------------------------

def config_add_actionsCorrespondence(actions):
    # Adds avatar actions correspondences
    for action in actions:
        if "AVATAR_ACTION_" in action.name:
            name = action.name.replace("AVATAR_ACTION_", "")

            if "USE" in name:
                correspondence = "ACTION_USE"
            elif "NIL" in name:
                correspondence = "ACTION_NIL"
            elif "UP" in name:
                correspondence = "ACTION_UP"
            elif "DOWN" in name:
                correspondence = "ACTION_DOWN"
            elif "LEFT" in name:
                correspondence = "ACTION_LEFT"
            elif "RIGHT" in name:
                correspondence = "ACTION_RIGHT"
            else:
                correspondence = None

            config["actionsCorrespondence"][action.name] = correspondence
        # In case we need to declare all actions
        # else:
        #     config["actionsCorrespondence"][action.name] = None

# ------------------------------------------------------------------------------

def config_add_additionalPredicates():
    pass

# ------------------------------------------------------------------------------

def config_add_addDeadObjects(partner, transformTo):
    # Objects the avatar can produce
    if partner:
        config["addDeadObjects"][partner.name] = 1

    # Objects that can be transformed
    for obj in transformTo:
        config["addDeadObjects"][obj] = 1
        # Make sure object is defined in variablesTypes
        config["variablesTypes"]["?%s" % obj] = obj

    # TODO: Add objects that can be produced (spawnpoints...)

# ------------------------------------------------------------------------------

# Only supporting SpriteCounter with limit=0
def config_add_goals(terminations):
    valid_goal = False

    # Search for the termination criteria
    for t in terminations:
        if t.type == "SpriteCounter" and t.win:
            valid_goal = True
            valid_termination = t

    # Check limit=0
    if valid_goal:
        parameters = [p for p in valid_termination.parameters if "limit=" in p]
        # If empty, assuming limit=0
        if not parameters:
            valid_goal = True
        else:
            limit = parameters[0].replace("limit=",'')
            valid_goal = limit == "0"

    if valid_goal:
        saveGoal = str("no")

        # Find sprite name
        parameters = [p for p in valid_termination.parameters if "stype=" in p]
        sprite = parameters[0].replace("stype=",'')

        config["goals"].append({
            "goalPredicate": "(forall (?o - {}) (object-dead ?o))".format(sprite),
            "priority": 1,
            "saveGoal": False
        })
    else:
        print("[WARNING]: The terminations criteria defined are not supported.\nA SpriteCounter with limit=0 is needed for an automatic generated goal.\n")
    