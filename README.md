# VGDL to HTN Parser

VGDL-to-HTN-Parser is a Python parser from VGDL game and level description into HPDL domains and problems.

``` This research is being developed and partially funded by the Spanish MINECO R&D Project TIN2015-71618-R and RTI2018-098460-B-I00 ```

# :unlock: Requirements
- Python3
- ANTLR 4.7.2 for Python3 (or superior), see [here](https://github.com/antlr/antlr4/blob/master/doc/python-target.md) for more information
- (For replanning only) Java JDK 8 (or superior)

# :wrench: Installation

Install ANTLR4 Python3 runtime:
```
pip install antlr4-python3-runtime
```


Compile Siadex planner (see the [README](planners/Siadex/README.md) for requirements):
```bash
$ make siadex-planner
```

# :computer: Usage

With the exception of the replanning module, all functionally can be called from the makefile.

The available options, with their parameters, are:
```
- help: Show help

For HPDL:
- hpdl-game: Parse only the VGDL description into a HPDL domain.
    gi: VGDL game description path.

- hpdl-level: Parse the VGDL description and a level
    gi: VGDL game description path.
    li: VGDL level path.


For HPDL execution with SIADEX:
- siadex-compile: Compile Siadex planner

- siadex-run: Call planner
    d: HPDL domain path
    p: HPDL problem path

- siadex-verbose: Call planner in verbose mode
    d: HPDL domain path
    p: HPDL problem path

- siadex-parse-and-run: Parse and call planner
    gi: VGDL game description path
    li: VGDL level path

For PDDL:
- pddl-game: Generate only the PDDL domain
  - gi: VGDL game description path
  - go: Output path

- config: Generate configuration and PDDL domain for a planning-based agent
  - gi: Path to VGDL description file
  - go: Name to be given to the output files
```

### PDDL parser

__Note__: Generation of PDDL levels is not yet completed, but domains in PPDL2.1 can be produced.

The PDDL parser was made for a planning-based agent (repo can be found [here](https://github.com/IgnacioVellido/VGDL-PDDL)). The subset of the VGDL language accepted is different from the HTN one, but nevertheless bigger, more efficient, and better tested. What's more, as in PDDL the planners handle the plan search, there is no need to define an agent strategy.

### Domain and problem generation
For domain and problem generation, you can use the makefile provided or directly the ```src/main.py``` script.

```bash
usage: main.py [-h] -l {pddl,hpdl} 
                    -gi GAMEINPUT 
                    [-li LEVELINPUT] 
                    [-go GAMEOUTPUT] 
                    [-lo LEVELOUTPUT] 
                    [-vh]

optional arguments:
  -h, --help            Show help message and exit
  -l {pddl,hpdl}, --language {pddl,hpdl}
                        Select output planning language
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
The HTN planner can be found in the [planners/Siadex](https://github.com/IgnacioVellido/VGDL-to-HTN-Parser/tree/master/planners/Siadex) directory.

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
__NOTE__: Only works on Linux

The replanning module is defined as a GVGAI agent, located [here](https://github.com/IgnacioVellido/VGDL-to-HTN-Parser/blob/master/replanning/GVGAI/src/main/Agent.java).
It uses a version of the GVGAI framework, from the official [repo](https://github.com/GAIGResearch/GVGAI).

The agent is available for the games __Sokoban__ (id=87), __Brainman__ (id=12), __Aliens__ (id=0) and __Boulderdash__ (id=83). The levels ids ranges from 0 to 4.

A basic configuration file is included under the ```replanning``` folder, where you can specify the game and the level to test.

&nbsp;

To run the agent, set the game id ant the level on ```replanning/configuration.txt``` and launch the java class ```/master/replanning/GVGAI/src/tracks/singlePlayer/Test.java```

You can also use an already defined domain setting the _KEEPDOMAIN_ variable in ```/master/replanning/GVGAI/src/main/Agent.java:20``` as __true__ and including it in the ```replanning/tmp``` folder with the name ```domain.hpdl```.

# :books: Results and experimentation

All related documentation and experimentation can be found under the [doc](https://github.com/IgnacioVellido/VGDL-to-HTN-Parser/tree/master/doc) directory.
