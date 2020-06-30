# VGDL to HTN Parser

VGDL-to-HTN-Parser is a Python parser from VGDL game and level description into HPDL domains and problems.

``` This research is being developed and partially funded by the Spanish MINECO R&D Project TIN2015-71618-R and RTI2018-098460-B-I00 ```

# Requirements
- Python3.
- ANTLR 4.7.2 for Python3 (or superior), see [here](https://github.com/antlr/antlr4/blob/master/doc/python-target.md) for more information.
- (For replanning only) Java JDK 8 (or superior).

# Installation
Compile Siadex planner:
```bash
$ make compile-planner
```

# Usage

With the exception of the replanning module, all functionally can be called from the  makefile.
<!-- The generation of domains/problems and plans (with the Siadex planner) is simplified with the use of  -->

```
The available options, with their parameters, are:

- parse-game: Parse only the VGDL description into a HPDL domain.
    gi: VGDL game description path.

- parse-level: Parse the VGDL description and a level
    gi: VGDL game description path.
    li: VGDL level path.

- help: Show help

- compile-planner: Compile Siadex planner

- run: Call planner
    d: HPDL domain path
    p: HPDL problem path

- verbose: Call planner in verbose mode
    d: HPDL domain path
    p: HPDL problem path

- parse-and-run: Parse and call planner
    gi: VGDL game description path.
    li: VGDL level path.
```


### Domain and problem generation
For domain and problem generation, you can use the makefile provided or directly the ```src/main.py``` script.

```bash
usage: main.py [-h] -gi GAMEINPUT [-li LEVELINPUT] [-go GAMEOUTPUT] [-lo LEVELOUTPUT] [-vh]

optional arguments:
  -h, --help            Show help message and exit
  -gi GAMEINPUT,    --gameInput GAMEINPUT
                        Input VGDL game file
  -li LEVELINPUT,   --levelInput LEVELINPUT
                        Input VGDL level file
  -go GAMEOUTPUT,   --gameOutput GAMEOUTPUT
                        Ouput VGDL game file
  -lo LEVELOUTPUT,  --levelOutput LEVELOUTPUT
                        Ouput VGDL level file
  -vh, --verboseHelp    Show additional information
```

### Planning with Siadex

```
Syntax: ./planner/planner [options] --domain_file (-d) <domain.pddl> --problem_file 
(-p) <problem.pddl>

Options:
        --help (-h):                      Shows this screen.
        --debug (-g):                     Runs the planner on debug mode.
        --verbose (-v[<level>] i.e: -v1): Sets on the verbose mode (1,2 o 3) (default 2).
        --output_file (-o) {filename}:    Writes resulting plan in a plain text file.
        --xml_file (-x) {filename}:       Writes resulting plan in xml format.
        --expansions_limit <number> :     Maximun number of allowed expansions.
        --depth_limit <number> :          Maximun depth during expansions.
        --time_limit <number> :           Maximun time of execution, in seconds.
        --seed (-s) <number> :            Random seed.

```

## Replanning module
The replanning module is defined as a GVGAI agent, located [here](https://github.com/IgnacioVellido/VGDL-to-HTN-Parser/blob/master/replanning/GVGAI/src/main/Agent.java).

The agent is available for the games Sokoban (id=87), Brainman (id=12), Aliens (id=0) and Boulderdash (id=83). The levels ids ranges from 0 to 4.

A basic configuration file is included under the ```replanning``` folder, where you can specify the game and the level to test.

To run the agent, just launch the java class ```/master/replanning/GVGAI/src/tracks/singlePlayer/Test.java```

# Results, experimentation and additional notes

- All related documentation and experimentation can be found under the [doc](https://github.com/IgnacioVellido/VGDL-to-HTN-Parser/tree/master/doc) directory.
  
- The replanning module uses a version of the GVGAI framework, from the [repo](https://github.com/GAIGResearch/GVGAI).
  
- The Siadex planner used for the experimentation can be found in the [planners/Siadex](https://github.com/IgnacioVellido/VGDL-to-HTN-Parser/tree/master/planners/Siadex) directory.