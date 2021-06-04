# Compile ANTLR grammar
compile-grammar:
	antlr4 -Dlanguage=Python3 Vgdl.g4

# Show help
help:
	python3 ./src/main.py -h

# ------------------------------------------------------------------------------
# PDDL
# ------------------------------------------------------------------------------

pddl-game:
	python3 ./src/main.py -l pddl -gi $(gi) -go $(go)

pddl-level:
	@echo "This functionality is not yet completed"

# For this repo: Generate PDDL domain and configuration file
config:
	python3 ./src/main.py -l pddl -c -gi $(gi) -go ../domains/simplified-version/$(go).pddl -co ../config/simplified-version/$(go).yaml
	
# ------------------------------------------------------------------------------
# HPDL
# ------------------------------------------------------------------------------

# Parse only the VGDL description
hpdl-game:
	python3 ./src/main.py -l hpdl -gi $(gi) -go ./output/domain.hpdl

# Parse the VGDL description and a level
hpdl-level:
	python3 ./src/main.py -l hpdl -gi $(gi) -li $(li) -go ./output/domain.hpdl -lo ./output/problem.hpdl

# ------------------------------------------------------------------------------
# SIADEX
# ------------------------------------------------------------------------------

siadex-compile:
	cd ./planners/Siadex && cmake . && cmake --build .

# Call planner
siadex-run:
	./planners/Siadex/planner -d $(d) -p $(p)

# Call planner in verbose mode
siadex-verbose:
	./planners/Siadex/planner -d $(d) -p $(p) -v

# For replanning: Parse and call planner
siadex-parse-and-run:
	python3 ./src/main.py -l hpdl -gi $(gi) -li $(li) -go ./output/domain.hpdl -lo ./output/problem.hpdl
	./planners/Siadex/planner -d ./output/domain.hpdl -p ./output/problem.hpdl

# ------------------------------------------------------------------------------
# Replanning
# ------------------------------------------------------------------------------

# Used in replanning: Parse and call planner keeping an already defined domain
replan-level:
	python3 ./src/main.py -l hpdl -gi $(gi) -li $(li) -go $(goTMP) -lo $(lo)
	./planners/Siadex/planner -d $(go) -p $(lo)
	# ./planners/Siadex/planner -d $(go) -p $(lo) 2> /dev/null

# For replanning: Parse and call planner
replan:
	python3 ./src/main.py -l hpdl  -gi $(gi) -li $(li) -go $(go) -lo $(lo)
	./planners/Siadex/planner -d $(go) -p $(lo)
	# ./planners/Siadex/planner -d $(go) -p $(lo) 2> /dev/null